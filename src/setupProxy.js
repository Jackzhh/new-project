// Setup proxy for React development server
const { spawn } = require('child_process');
const path = require('path');

// 执行 MCP PostgreSQL 查询
function executeMCPQuery(sql) {
  return new Promise((resolve, reject) => {
    // setupProxy.js 在 src/ 目录下，需要回到项目根目录
    const clientPath = path.resolve(__dirname, '..', 'mcp-postgres-client.js');
    console.log('🔍 MCP client path:', clientPath);
    const child = spawn('node', [clientPath, sql]);
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (parseError) {
          reject(new Error('Failed to parse MCP response: ' + parseError.message));
        }
      } else {
        reject(new Error('MCP client failed: ' + stderr));
      }
    });
    
    child.on('error', (error) => {
      reject(new Error('Failed to spawn MCP client: ' + error.message));
    });
  });
}

module.exports = function(app) {
  // 添加 JSON 解析中间件
  app.use('/api', require('express').json());
  
  // 处理数据库查询请求
  app.post('/api/query', async (req, res) => {
    try {
      console.log('📨 Received API request:', req.body);
      const { sql } = req.body;
      
      if (!sql) {
        console.log('❌ No SQL provided');
        return res.status(400).json({ error: 'SQL query is required' });
      }
      
      console.log('🔄 Executing SQL:', sql.substring(0, 100) + '...');
      const result = await executeMCPQuery(sql);
      console.log('✅ Query successful:', result);
      res.json(result);
      
    } catch (error) {
      console.error('❌ Database query error:', error);
      console.error('❌ Error stack:', error.stack);
      res.status(500).json({ 
        error: 'Database query failed', 
        details: error.message 
      });
    }
  });
};
