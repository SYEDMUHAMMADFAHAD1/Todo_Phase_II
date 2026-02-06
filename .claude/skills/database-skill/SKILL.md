---
name: database-skill
description: Design robust database schemas, create tables, and manage migrations for scalable applications.
---

# Database Skill – Schema Design & Migrations

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize tables (avoid redundancy)
   - Choose appropriate data types
   - Define primary keys and foreign keys

2. **Table Creation**
   - Use clear, consistent naming conventions
   - Add constraints (NOT NULL, UNIQUE)
   - Define indexes for frequently queried columns
   - Include timestamps where needed

3. **Migrations**
   - Create reversible migration files
   - Separate schema changes into small steps
   - Version and track migrations
   - Test migrations in staging before production

4. **Data Integrity**
   - Enforce referential integrity
   - Use transactions for multi-step operations
   - Apply cascading rules carefully (ON DELETE / ON UPDATE)

---

## Best Practices
- Prefer explicit schemas over implicit behavior
- Keep tables focused on a single responsibility
- Avoid premature optimization, but add indexes intentionally
- Document schema decisions
- Back up data before running destructive migrations
- Use environment-specific databases (dev / staging / prod)

---

## Example Structure

### Example: Users & Posts Schema (SQL)

```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
