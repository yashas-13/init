Here is a detailed database (DB) setup plan for your in-house pharmaceutical supply chain management application, designed for a completely local setup using a relational database model (like SQLite, as previously discussed). This schema incorporates all the required aspects for the app, including hierarchical user management, batch-wise product operations, and multi-step approvals, drawing directly from the functionalities outlined in the research.

Each table definition includes:

* **Table Name**: A clear and descriptive name.  
* **Purpose**: A brief explanation of what the table stores.  
* **Columns**: A list of columns with their data types (using common SQL types) and constraints (e.g., PRIMARY KEY, NOT NULL, UNIQUE, FOREIGN KEY).  
* **Relationships**: How the table connects to other tables.

## ---

**Detailed Database Schema for Local Pharma SCM App**

This schema is designed to support the core functionalities of your pharmaceutical supply chain management application, including manufacturer, CFA, and stockist operations, batch tracking, and approval workflows.

### **1\. Organizations Table**

* **Purpose**: Stores details for all organizational entities in the supply chain: the Manufacturer, Carrying and Forwarding Agents (CFAs), and Stockists. This table forms the basis for hierarchical relationships and linking users to their respective companies.  
* **Columns**:  
  * organization\_id (TEXT PRIMARY KEY): A unique identifier for each organization (e.g., 'MANUF001', 'CFA001', 'STOCKIST001').  
  * name (TEXT NOT NULL): The official name of the organization (e.g., 'PharmaCo Inc.', 'Central Pharma CFA', 'City Drug Store').  
  * type (TEXT NOT NULL): The classification of the organization ('Manufacturer', 'CFA', 'Stockist').  
  * address (TEXT): Street address of the organization.  
  * city (TEXT): City of the organization.  
  * state (TEXT): State/Province of the organization.  
  * country (TEXT): Country of the organization.  
  * postal\_code (TEXT): Postal code of the organization.  
  * phone (TEXT): Primary contact phone number for the organization.  
  * fax (TEXT): Fax number for the organization (optional).  
  * email (TEXT): General contact email for the organization.  
  * parent\_organization\_id (TEXT): Foreign Key referencing Organizations.organization\_id. Used to establish hierarchical relationships (e.g., a CFA belonging to a Manufacturer, or a Stockist belonging to a CFA). Can be NULL for top-level organizations. 1  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the record was created.  
  * updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to the record.

### **2\. Users Table**

* **Purpose**: Stores individual user accounts, their login credentials, and their assigned roles within an organization. This supports the manufacturer's ability to create and manage all CFA and stockist accounts. 3  
* **Columns**:  
  * user\_id (TEXT PRIMARY KEY): A unique identifier for each user (e.g., 'USR001').  
  * organization\_id (TEXT NOT NULL): Foreign Key referencing Organizations.organization\_id. Links the user to their respective organization.  
  * email (TEXT NOT NULL UNIQUE): The user's unique email address, used for login.  
  * password\_hash (TEXT NOT NULL): A secure hash of the user's password.  
  * first\_name (TEXT): User's first name.  
  * last\_name (TEXT): User's last name.  
  * role (TEXT NOT NULL): The user's role within the application, determining their access and permissions (e.g., 'manufacturer\_admin', 'cfa\_manager', 'cfa\_operator', 'stockist\_admin', 'stockist\_clerk'). 3  
  * status (TEXT DEFAULT 'active'): Current status of the user account ('active', 'inactive', 'pending').  
  * last\_login\_at (DATETIME): Timestamp of the user's last successful login.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the user account was created.  
  * updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to the user record.

### **3\. Products Table**

* **Purpose**: Stores master data for each unique pharmaceutical product manufactured or handled.  
* **Columns**:  
  * product\_id (TEXT PRIMARY KEY): A unique identifier for each product (e.g., 'PROD001').  
  * name (TEXT NOT NULL): The commercial name of the product (e.g., 'PainRelief 500mg').  
  * sku (TEXT NOT NULL UNIQUE): Stock Keeping Unit, a unique identifier for the product type.  
  * description (TEXT): A brief description of the product.  
  * unit\_of\_measure (TEXT): The standard unit for the product (e.g., 'tablet', 'bottle', 'box').  
  * manufacturer\_org\_id (TEXT): Foreign Key referencing Organizations.organization\_id. Identifies the primary manufacturer of this product.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the product record was created.  
  * updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to the product record.

### **4\. Batches Table**

* **Purpose**: Stores detailed information for each specific production batch of a pharmaceutical product, crucial for batch-wise tracking and traceability. 5  
* **Columns**:  
  * batch\_id (TEXT PRIMARY KEY): A unique identifier for each batch (e.g., 'BATCH001-PROD001').  
  * product\_id (TEXT NOT NULL): Foreign Key referencing Products.product\_id. Links the batch to its product master data.  
  * batch\_number (TEXT NOT NULL): The actual alphanumeric batch number assigned during manufacturing (e.g., 'A1-23W42').  
  * manufacturing\_date (DATE): The date the batch was manufactured.  
  * expiry\_date (DATE): The expiration date of the batch.  
  * manufacturing\_site\_name (TEXT): The name or identifier of the manufacturing facility.  
  * quality\_control\_status (TEXT DEFAULT 'Released'): Current quality status of the batch ('Released', 'On Hold', 'Rejected', 'Recalled'). 7  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the batch record was created.  
  * updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to the batch record.  
* **Constraint**: UNIQUE(product\_id, batch\_number): Ensures that a specific batch number is unique for a given product.

### **5\. Inventory Table**

* **Purpose**: Tracks the current quantity of each product batch at specific locations (Manufacturer warehouse, CFA warehouse, Stockist locations).  
* **Columns**:  
  * inventory\_record\_id (TEXT PRIMARY KEY): A unique identifier for each inventory record.  
  * organization\_id (TEXT NOT NULL): Foreign Key referencing Organizations.organization\_id. Represents the organization currently holding this inventory (the location/owner).  
  * product\_id (TEXT NOT NULL): Foreign Key referencing Products.product\_id.  
  * batch\_id (TEXT NOT NULL): Foreign Key referencing Batches.batch\_id.  
  * quantity (INTEGER NOT NULL): The current quantity of this specific batch at this location.  
  * storage\_condition (TEXT): Describes the required storage conditions (e.g., 'Ambient', 'Refrigerated', 'Frozen'). 8  
  * last\_updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to this inventory record.  
* **Constraint**: UNIQUE(organization\_id, batch\_id): Ensures there is only one inventory record for a specific batch at a given organization/location.

### **6\. Requests Table**

* **Purpose**: Stores details of various requests initiated by CFAs or Stockists that require manufacturer approval (e.g., dispatch requests, returns, inventory adjustments).  
* **Columns**:  
  * request\_id (TEXT PRIMARY KEY): A unique identifier for each request.  
  * request\_type (TEXT NOT NULL): The type of request ('Dispatch', 'Return', 'Inventory Adjustment', 'Quality Hold Release'). 7  
  * initiator\_user\_id (TEXT NOT NULL): Foreign Key referencing Users.user\_id. The user who created this request.  
  * initiator\_org\_id (TEXT NOT NULL): Foreign Key referencing Organizations.organization\_id. The organization of the user who created the request.  
  * target\_org\_id (TEXT): Foreign Key referencing Organizations.organization\_id. The target organization for the request (e.g., destination for a dispatch, source for a return). Can be NULL for internal adjustments.  
  * status (TEXT DEFAULT 'Pending'): Current status of the request ('Pending', 'Approved', 'Rejected', 'In Progress', 'Completed', 'Cancelled'). 9  
  * request\_date (DATETIME DEFAULT CURRENT\_TIMESTAMP): Date and time the request was initiated.  
  * completion\_date (DATETIME): Date and time the request was fully completed or resolved.  
  * notes (TEXT): Any additional notes or comments related to the request.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the request record was created.  
  * updated\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp of the last update to the request record.

### **7\. Request\_Items Table**

* **Purpose**: Details the specific products and batches involved in a Requests record. A single request can involve multiple products/batches.  
* **Columns**:  
  * request\_item\_id (TEXT PRIMARY KEY): A unique identifier for each item within a request.  
  * request\_id (TEXT NOT NULL): Foreign Key referencing Requests.request\_id.  
  * product\_id (TEXT NOT NULL): Foreign Key referencing Products.product\_id.  
  * batch\_id (TEXT NOT NULL): Foreign Key referencing Batches.batch\_id.  
  * requested\_quantity (INTEGER NOT NULL): The quantity of the product/batch requested.  
  * approved\_quantity (INTEGER): The quantity approved by the manufacturer (can differ from requested\_quantity).  
  * unit\_price (REAL): Optional, for financial tracking per unit.  
  * notes (TEXT): Specific notes for this request item.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the request item record was created.

### **8\. Approvals Table**

* **Purpose**: Records each step of a multi-step approval process for a Requests record, ensuring traceability and accountability for decisions. 7  
* **Columns**:  
  * approval\_record\_id (TEXT PRIMARY KEY): A unique identifier for each approval step.  
  * request\_id (TEXT NOT NULL): Foreign Key referencing Requests.request\_id.  
  * approver\_user\_id (TEXT NOT NULL): Foreign Key referencing Users.user\_id. The user who performed this approval/rejection.  
  * approval\_step (INTEGER NOT NULL): The sequential order of this approval in the workflow (e.g., 1, 2, 3).  
  * status (TEXT NOT NULL): The outcome of this specific approval step ('Approved', 'Rejected', 'Pending' if it's the current step).  
  * approval\_date (DATETIME DEFAULT CURRENT\_TIMESTAMP): Date and time the approval/rejection was made.  
  * rationale (TEXT): The reason or comments provided for the approval/rejection.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the approval record was created.  
* **Constraint**: UNIQUE(request\_id, approval\_step): Ensures that each approval step for a given request is unique.

### **9\. Transactions Table**

* **Purpose**: An immutable log of all actual physical movements and significant status changes of products (e.g., dispatch, receipt, inventory adjustments, quality holds/releases). This is the core traceability log. 11  
* **Columns**:  
  * transaction\_id (TEXT PRIMARY KEY): A unique identifier for each transaction.  
  * request\_id (TEXT): Foreign Key referencing Requests.request\_id. Links the transaction to an approved request (can be NULL for direct adjustments not tied to a formal request).  
  * product\_id (TEXT NOT NULL): Foreign Key referencing Products.product\_id.  
  * batch\_id (TEXT NOT NULL): Foreign Key referencing Batches.batch\_id.  
  * quantity (INTEGER NOT NULL): The quantity of the product/batch involved in the transaction.  
  * transaction\_type (TEXT NOT NULL): The nature of the transaction ('Dispatch', 'Receipt', 'Inventory Adjustment (Add)', 'Inventory Adjustment (Subtract)', 'Quality Hold', 'Quality Release', 'Return In', 'Return Out').  
  * source\_org\_id (TEXT): Foreign Key referencing Organizations.organization\_id. The organization from which the product moved (can be NULL for new production).  
  * destination\_org\_id (TEXT): Foreign Key referencing Organizations.organization\_id. The organization to which the product moved (can be NULL for destruction).  
  * transaction\_date (DATETIME DEFAULT CURRENT\_TIMESTAMP): Date and time the transaction occurred.  
  * recorded\_by\_user\_id (TEXT NOT NULL): Foreign Key referencing Users.user\_id. The user who recorded this transaction.  
  * notes (TEXT): Any additional notes about the transaction.  
  * created\_at (DATETIME DEFAULT CURRENT\_TIMESTAMP): Timestamp when the transaction record was created.

### **10\. Audit\_Logs Table**

* **Purpose**: Provides a comprehensive, immutable, and tamper-proof log of all significant system-level actions and data changes for compliance, accountability, and debugging. 7  
* **Columns**:  
  * log\_id (TEXT PRIMARY KEY): A unique identifier for each log entry.  
  * user\_id (TEXT): Foreign Key referencing Users.user\_id. The user who performed the action (can be NULL for system-initiated actions).  
  * action\_type (TEXT NOT NULL): Describes the type of action (e.g., 'User Created', 'Organization Updated', 'Product Added', 'Batch Status Change', 'Request Status Change', 'Login Success', 'Login Failed').  
  * table\_name (TEXT): The name of the database table affected by the action (e.g., 'Users', 'Organizations', 'Requests').  
  * record\_id (TEXT): The primary key ID of the specific record affected in table\_name.  
  * old\_value (TEXT): A JSON string representing the state of the record *before* the change (optional, for detailed auditing).  
  * new\_value (TEXT): A JSON string representing the state of the record *after* the change (optional, for detailed auditing).  
  * timestamp (DATETIME DEFAULT CURRENT\_TIMESTAMP): The exact date and time the action was logged.

---

This detailed schema provides a robust foundation for your local Python mobile application, enabling comprehensive management of your pharmaceutical supply chain operations.