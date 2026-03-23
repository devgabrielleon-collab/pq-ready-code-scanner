const crypto = require('crypto');

const tlsProfile = {
  cert: './tls/server.crt',
  key: './tls/server.key',
  kex: 'curve25519-sha256',
};

console.log(crypto, tlsProfile);
