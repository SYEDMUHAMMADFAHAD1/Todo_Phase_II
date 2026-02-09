# Data Model: Chatbot UI & Stateless Chat API Foundation

## Entities

### Conversation
**Description**: Represents a logical grouping of messages between a user and the AI assistant

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the conversation
- user_id: String - Identifier of the user who owns this conversation
- created_at: DateTime - Timestamp when the conversation was initiated
- updated_at: DateTime - Timestamp when the conversation was last updated
- title: String (Optional) - Auto-generated title based on first message or topic

**Validation Rules**:
- user_id must correspond to an existing user
- created_at must be in the past
- updated_at must be >= created_at

**Relationships**:
- One-to-many with Message (one conversation has many messages)
- Belongs to User (via user_id foreign key)

### Message
**Description**: Represents a single exchange in a conversation

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the message
- conversation_id: UUID - Foreign key linking to parent conversation
- role: String (Enum: 'user' | 'assistant') - Specifies who sent the message
- content: Text - The actual message content
- created_at: DateTime - Timestamp when the message was created
- updated_at: DateTime - Timestamp when the message was last updated

**Validation Rules**:
- conversation_id must correspond to an existing conversation
- role must be either 'user' or 'assistant'
- content must not be empty
- created_at must be in the past
- updated_at must be >= created_at

**Relationships**:
- Many-to-one with Conversation (many messages belong to one conversation)

### User
**Description**: The authenticated entity that owns conversations

**Fields**:
- id: String - Unique user identifier (from Better Auth)
- email: String - User's email address
- created_at: DateTime - When the user account was created
- updated_at: DateTime - When the user account was last updated

**Validation Rules**:
- email must be a valid email format
- id must be unique

**Relationships**:
- One-to-many with Conversation (one user has many conversations)

## State Transitions

### Conversation Lifecycle
1. **Creation**: New conversation initiated when user starts chatting
2. **Active**: Messages are added to the conversation
3. **Inactive**: Conversation hasn't been updated for a period (optional cleanup)

### Message Lifecycle
1. **Pending**: Message sent by user, waiting for AI response
2. **Processing**: AI is generating response
3. **Complete**: Both user message and AI response are stored

## Database Constraints

1. **Foreign Key Integrity**: All foreign key relationships enforced at database level
2. **User Isolation**: Queries must always filter by authenticated user_id to prevent cross-user access
3. **Chronological Order**: Messages should be retrieved with ORDER BY created_at ASC
4. **Unique Ownership**: Users can only access conversations they own (enforced by application logic and database queries)

## Indexing Strategy

1. **conversations.user_id**: Index for efficient user-specific queries
2. **messages.conversation_id**: Index for efficient conversation history retrieval
3. **messages.created_at**: Index for chronological ordering
4. **messages.conversation_id_created_at**: Composite index for efficient conversation history with chronological order