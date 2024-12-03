### **README**

---

#### **Project Overview**
This project implements a simple multithreaded HTTP server in Python that can handle basic GET and POST requests. It allows clients to interact with files stored in a specified directory and provides functionalities such as serving static content, echoing data, and handling user-agent headers.

---

#### **Features**
1. **GET Requests**:
   - Retrieve files from the specified directory.
   - Serve static responses for root and `/index.html`.

2. **POST Requests**:
   - Create new files in the specified directory with the content provided in the request body.

3. **Additional Endpoints**:
   - `/echo/{data}`: Echo back the provided data.
   - `/user-agent`: Respond with the client’s `User-Agent` header.

4. **Error Handling**:
   - Respond with appropriate HTTP status codes such as `404 Not Found` and `400 Bad Request`.

5. **Multithreading**:
   - Each client request is handled in a separate thread to allow concurrent processing.

---

#### **Setup Instructions**
1. **Prerequisites**:
   - Python 3.7 or higher installed on your system.
   - Basic knowledge of HTTP methods.

2. **Run the Server**:
   - Clone or download the repository.
   - Navigate to the `app` directory:
     ```bash
     cd app
     ```
   - Start the server with the required directory:
     ```bash
     python main.py --directory /path/to/your/directory
     ```
   - Replace `/path/to/your/directory` with the absolute path to the directory where files will be served or stored.

3. **Test the Server**:
   - Use `curl` or a browser to test endpoints:
     ```bash
     curl -i http://localhost:4221/
     curl -i http://localhost:4221/files/filename
     curl -v --data "test content" -H "Content-Type: text/plain" http://localhost:4221/files/newfile
     ```

---

#### **Endpoints**
1. **Root (`/`)**:
   - Response: `Hello, World!`
   - Example:
     ```bash
     curl -i http://localhost:4221/
     ```

2. **Static File (`/files/{filename}`)**:
   - GET: Retrieve a file from the directory.
   - POST: Create a file in the directory with request body content.
   - Example:
     ```bash
     curl -i http://localhost:4221/files/test.txt
     curl -v --data "example content" http://localhost:4221/files/newfile.txt
     ```

3. **Echo (`/echo/{data}`)**:
   - Responds with the `{data}` provided in the path.
   - Example:
     ```bash
     curl -i http://localhost:4221/echo/hello
     ```

4. **User-Agent (`/user-agent`)**:
   - Responds with the `User-Agent` header sent by the client.
   - Example:
     ```bash
     curl -H "User-Agent: MyTestAgent" http://localhost:4221/user-agent
     ```

---

#### **Error Codes**
- **400 Bad Request**: Invalid or malformed request.
- **404 Not Found**: Resource not found.
- **500 Internal Server Error**: Server error while processing the request.

---

#### **Known Limitations**
- This server is single-directory scoped and cannot handle subdirectories.
- Limited to basic HTTP features; lacks HTTPS support.

---

#### **Contributors**
- **Medhansh Choubey**
