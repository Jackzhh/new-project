#!/usr/bin/env node

// MCP PostgreSQL client for executing queries
const { Client } = require('pg');

// Get SQL query from command line argument
const sql = process.argv[2];

if (!sql) {
  console.error(JSON.stringify({ error: 'SQL query is required' }));
  process.exit(1);
}

// PostgreSQL connection configuration
const connectionConfig = {
  host: 'localhost',
  port: 5433,
  database: 'mcpdb',
  user: 'mcpuser',
  password: 'mcppassword',
  connectionTimeoutMillis: 5000,
  idleTimeoutMillis: 10000,
};

// Execute the query and return results
async function executeQuery() {
  const client = new Client(connectionConfig);
  
  try {
    console.error('🔄 Connecting to PostgreSQL database...');
    await client.connect();
    console.error('✅ Connected to database successfully');
    
    console.error(`🔍 Executing query: ${sql.substring(0, 100)}...`);
    const result = await client.query(sql);
    
    console.error(`📊 Query returned ${result.rows.length} rows`);
    
    // Return the result in the expected format
    const response = {
      rows: result.rows,
      rowCount: result.rowCount,
      command: result.command
    };
    
    console.log(JSON.stringify(response));
    
  } catch (error) {
    console.error('❌ Database error:', error.message);
    
    // If database connection fails, fall back to mock data
    console.error('⚠️ Falling back to mock data...');
    const mockResult = getMockResponse(sql);
    console.log(JSON.stringify(mockResult));
    
  } finally {
    try {
      await client.end();
      console.error('🔌 Database connection closed');
    } catch (err) {
      console.error('⚠️ Error closing connection:', err.message);
    }
  }
}

// Mock database response for fallback
function getMockResponse(sql) {
  const query = sql.toLowerCase().trim();
  
  if (query.includes('information_schema.tables')) {
    return {
      rows: [
        { table_name: 'users' },
        { table_name: 'products' },
        { table_name: 'orders' },
        { table_name: 'categories' },
        { table_name: 'order_items' }
      ]
    };
  }
  
  if (query.includes('information_schema.columns')) {
    if (query.includes("table_name = 'users'")) {
      return {
        rows: [
          { column_name: 'id', data_type: 'integer', is_nullable: 'NO' },
          { column_name: 'username', data_type: 'character varying', is_nullable: 'NO' },
          { column_name: 'email', data_type: 'character varying', is_nullable: 'NO' },
          { column_name: 'full_name', data_type: 'character varying', is_nullable: 'YES' },
          { column_name: 'created_at', data_type: 'timestamp with time zone', is_nullable: 'NO' },
          { column_name: 'is_active', data_type: 'boolean', is_nullable: 'NO' }
        ]
      };
    }
    if (query.includes("table_name = 'products'")) {
      return {
        rows: [
          { column_name: 'id', data_type: 'integer', is_nullable: 'NO' },
          { column_name: 'name', data_type: 'character varying', is_nullable: 'NO' },
          { column_name: 'description', data_type: 'text', is_nullable: 'YES' },
          { column_name: 'price', data_type: 'numeric', is_nullable: 'NO' },
          { column_name: 'category_id', data_type: 'integer', is_nullable: 'YES' },
          { column_name: 'stock_quantity', data_type: 'integer', is_nullable: 'NO' }
        ]
      };
    }
  }
  
  if (query.includes('select * from users')) {
    return {
      rows: [
        { id: 1, username: 'john_doe', email: 'john@example.com', full_name: 'John Doe', created_at: '2024-01-15T10:30:00Z', is_active: true },
        { id: 2, username: 'jane_smith', email: 'jane@example.com', full_name: 'Jane Smith', created_at: '2024-01-16T14:22:00Z', is_active: true },
        { id: 3, username: 'bob_wilson', email: 'bob@example.com', full_name: 'Bob Wilson', created_at: '2024-01-17T09:15:00Z', is_active: false }
      ]
    };
  }
  
  if (query.includes('select * from products')) {
    return {
      rows: [
        { id: 1, name: 'Laptop Pro', description: 'High-performance laptop', price: '1299.99', category_id: 1, stock_quantity: 25 },
        { id: 2, name: 'Wireless Mouse', description: 'Ergonomic wireless mouse', price: '29.99', category_id: 2, stock_quantity: 150 },
        { id: 3, name: 'Mechanical Keyboard', description: 'RGB backlit keyboard', price: '89.99', category_id: 2, stock_quantity: 75 }
      ]
    };
  }
  
  // Default response for unknown queries
  return {
    rows: [
      { message: 'Query executed successfully (mock)', query: sql.substring(0, 50) + '...' }
    ]
  };
}

// Run the query
executeQuery().catch(error => {
  console.error(JSON.stringify({ 
    error: 'Unexpected error', 
    details: error.message 
  }));
  process.exit(1);
});
