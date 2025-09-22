#!/usr/bin/env node

/**
 * Script de inicialización de la base de datos IBM Quality Management
 * Crea la base de datos, esquemas, tablas y datos iniciales
 */

const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

// Configuración de conexión
const config = {
    user: process.env.DB_USER || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    password: process.env.DB_PASSWORD || 'postgres',
    port: process.env.DB_PORT || 5432,
};

const dbName = 'ibm_quality_management';

async function initializeDatabase() {
    console.log('🚀 Iniciando configuración de la base de datos IBM Quality Management...\n');
    
    // Conectar a PostgreSQL sin especificar base de datos
    const adminPool = new Pool(config);
    
    try {
        // 1. Verificar si la base de datos existe
        console.log('1️⃣ Verificando si la base de datos existe...');
        const dbExists = await adminPool.query(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            [dbName]
        );
        
        if (dbExists.rows.length === 0) {
            console.log(`   ➕ Creando base de datos '${dbName}'...`);
            await adminPool.query(`CREATE DATABASE ${dbName}`);
            console.log('   ✅ Base de datos creada exitosamente');
        } else {
            console.log('   ✅ Base de datos ya existe');
        }
        
        await adminPool.end();
        
        // 2. Conectar a la base de datos específica
        console.log('\n2️⃣ Conectando a la base de datos...');
        const dbPool = new Pool({
            ...config,
            database: dbName
        });
        
        // 3. Leer y ejecutar el schema SQL
        console.log('3️⃣ Ejecutando schema de la base de datos...');
        const schemaPath = path.join(__dirname, '..', 'database', 'schema.sql');
        
        if (fs.existsSync(schemaPath)) {
            const schemaSql = fs.readFileSync(schemaPath, 'utf8');
            
            // Dividir en statements individuales (ignorar líneas de comentarios y conexiones)
            const statements = schemaSql
                .split(';')
                .map(stmt => stmt.trim())
                .filter(stmt => 
                    stmt.length > 0 && 
                    !stmt.startsWith('--') && 
                    !stmt.startsWith('\\c') &&
                    !stmt.startsWith('CREATE DATABASE')
                );
            
            console.log(`   📝 Ejecutando ${statements.length} statements...`);
            
            for (let i = 0; i < statements.length; i++) {
                const statement = statements[i];
                if (statement.trim()) {
                    try {
                        await dbPool.query(statement);
                        console.log(`   ✅ Statement ${i + 1}/${statements.length} ejecutado`);
                    } catch (error) {
                        if (error.message.includes('already exists')) {
                            console.log(`   ⚠️ Statement ${i + 1}: ${error.message}`);
                        } else {
                            console.log(`   ❌ Error en statement ${i + 1}: ${error.message}`);
                        }
                    }
                }
            }
        } else {
            console.log('   ⚠️ Archivo schema.sql no encontrado, creando estructura básica...');
            await createBasicSchema(dbPool);
        }
        
        // 4. Insertar datos iniciales
        console.log('\n4️⃣ Insertando datos iniciales...');
        await insertInitialData(dbPool);
        
        // 5. Verificar instalación
        console.log('\n5️⃣ Verificando instalación...');
        await verifyInstallation(dbPool);
        
        await dbPool.end();
        
        console.log('\n🎉 Base de datos IBM Quality Management configurada exitosamente!');
        console.log('📊 El sistema está listo para recibir datos de defectos.');
        
    } catch (error) {
        console.error('❌ Error configurando la base de datos:', error);
        process.exit(1);
    }
}

async function createBasicSchema(pool) {
    const basicTables = [
        `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`,
        `CREATE EXTENSION IF NOT EXISTS "pg_trgm"`,
        
        `CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )`,
        
        `CREATE TABLE IF NOT EXISTS projects (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            code VARCHAR(20) UNIQUE NOT NULL,
            description TEXT,
            status VARCHAR(30) DEFAULT 'active',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )`,
        
        `CREATE TABLE IF NOT EXISTS defects (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            defect_id VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
            priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
            status VARCHAR(30) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed', 'rejected')),
            type VARCHAR(50),
            found_in_environment VARCHAR(50),
            project_id UUID REFERENCES projects(id),
            reported_by UUID REFERENCES users(id),
            assigned_to UUID REFERENCES users(id),
            steps_to_reproduce JSONB,
            expected_behavior TEXT,
            actual_behavior TEXT,
            resolution TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )`,
        
        `CREATE TABLE IF NOT EXISTS activity_logs (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id),
            action VARCHAR(100) NOT NULL,
            entity_type VARCHAR(50),
            entity_id UUID,
            details JSONB,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )`
    ];
    
    for (const sql of basicTables) {
        try {
            await pool.query(sql);
            console.log('   ✅ Tabla creada');
        } catch (error) {
            console.log(`   ⚠️ ${error.message}`);
        }
    }
}

async function insertInitialData(pool) {
    // Insertar usuario administrador por defecto
    try {
        const adminUser = await pool.query(`
            INSERT INTO users (username, email, full_name, role)
            VALUES ('admin', 'admin@ibm.com', 'Administrador del Sistema', 'admin')
            ON CONFLICT (username) DO NOTHING
            RETURNING id
        `);
        
        if (adminUser.rows.length > 0) {
            console.log('   ✅ Usuario administrador creado');
        } else {
            console.log('   ✅ Usuario administrador ya existe');
        }
    } catch (error) {
        console.log('   ⚠️ Error creando usuario administrador:', error.message);
    }
    
    // Insertar proyecto de ejemplo
    try {
        const project = await pool.query(`
            INSERT INTO projects (name, code, description)
            VALUES ('IBM Quality Management', 'IBM-QM', 'Sistema de gestión de calidad IBM')
            ON CONFLICT (code) DO NOTHING
            RETURNING id
        `);
        
        if (project.rows.length > 0) {
            console.log('   ✅ Proyecto de ejemplo creado');
        } else {
            console.log('   ✅ Proyecto de ejemplo ya existe');
        }
    } catch (error) {
        console.log('   ⚠️ Error creando proyecto:', error.message);
    }
    
    // Insertar usuarios de ejemplo
    const sampleUsers = [
        ['qa_manager', 'qa.manager@ibm.com', 'Manager de QA', 'quality_manager'],
        ['qa_engineer', 'qa.engineer@ibm.com', 'Ingeniero QA', 'qa_engineer'],
        ['developer', 'developer@ibm.com', 'Desarrollador', 'developer'],
        ['tester', 'tester@ibm.com', 'Tester', 'qa_engineer']
    ];
    
    for (const [username, email, fullName, role] of sampleUsers) {
        try {
            await pool.query(`
                INSERT INTO users (username, email, full_name, role)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (username) DO NOTHING
            `, [username, email, fullName, role]);
            console.log(`   ✅ Usuario ${username} creado`);
        } catch (error) {
            console.log(`   ⚠️ Usuario ${username} ya existe`);
        }
    }
}

async function verifyInstallation(pool) {
    try {
        // Verificar tablas principales
        const tables = await pool.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        `);
        
        console.log(`   📋 Tablas creadas: ${tables.rows.length}`);
        tables.rows.forEach(row => {
            console.log(`      - ${row.table_name}`);
        });
        
        // Verificar usuarios
        const userCount = await pool.query('SELECT COUNT(*) FROM users');
        console.log(`   👥 Usuarios creados: ${userCount.rows[0].count}`);
        
        // Verificar proyectos
        const projectCount = await pool.query('SELECT COUNT(*) FROM projects');
        console.log(`   📁 Proyectos creados: ${projectCount.rows[0].count}`);
        
        // Verificar defectos
        const defectCount = await pool.query('SELECT COUNT(*) FROM defects');
        console.log(`   🐛 Defectos existentes: ${defectCount.rows[0].count}`);
        
    } catch (error) {
        console.log('   ❌ Error verificando instalación:', error.message);
    }
}

// Ejecutar si se llama directamente
if (require.main === module) {
    initializeDatabase();
}

module.exports = { initializeDatabase };