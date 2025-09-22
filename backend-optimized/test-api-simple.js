const http = require('http');

// Test GET defects
const getOptions = {
  hostname: 'localhost',
  port: 3003,
  path: '/api/v1/defects',
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
};

console.log('🔍 Probando GET /api/v1/defects...');

const req = http.request(getOptions, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers: ${JSON.stringify(res.headers)}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('Response body:');
    try {
      const parsed = JSON.parse(data);
      console.log(JSON.stringify(parsed, null, 2));
    } catch (e) {
      console.log('Raw response:', data);
    }
  });
});

req.on('error', (err) => {
  console.error('Error:', err.message);
});

req.end();