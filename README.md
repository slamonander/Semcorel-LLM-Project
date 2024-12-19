# CSE 120
## Team 317 - semcorel Inc.
## Use-Case
![Use-Case](https://github.com/user-attachments/assets/1b1a81e2-b803-4577-b734-4f5c92cf3f26)


## Class Diagram
![Class Diagram](https://github.com/user-attachments/assets/1d46edad-08aa-47e6-b548-5d5a30c30973)
# Project Setup Instructions

# Project Setup Instructions

This README provides instructions to set up the **frontend**, **backend**, **admin view**, and the **iOS WebView app** for this project. Follow the steps below to ensure everything works correctly.

Frontend Setup:  
**Navigate to the Frontend Directory:**  
`cd final/frontend  `

**Build and Start the Frontend:**  
`npm run build; npm start  `

**Note:** The link generated after running the above commands will **not** be directly used in the iOS WebView app. Ensure to continue with the backend setup to obtain the correct link.

Backend Setup:  
**Navigate to the Backend Directory:**  
`cd final/backend  `

**Install Dependencies:**  
`pip3 install -r requirements.txt  `

**Start the Backend:**  
`python3 app.py  `

**Note:** The backend uses **flask_cors** to generate an IP-based link. Copy this generated link as it will be used in the iOS WebView app setup. The backend runs on port **8080**.

**Admin View Setup:**

Navigate to the Admin Directory:
`cd final/admin  `

**Install Dependencies:**  
`pip3 install -r requirements.txt  `

**Start the Admin View:**  
`python3 admin.py  `

iOS WebView App Setup:  
**Update the WebView URL in the iOS App:**  

Example:  
URLWebView(urlString: "http://xxx.xxx.xx.x:8080/")  

Replace `xxx.xxx.xx.x` with the actual IP address provided by the backend setup (from the Flask server). Ensure that port **8080** is used, as it corresponds to the backend Python server.  

**Recompile the iOS app** to ensure the updated WebView URL is applied.

Key Notes:  
- The IP address from the backend link must be accessible by the iOS app.  
- Ensure the iOS app has proper permissions and configurations for network access.

Summary:  
- **Frontend:** Build and run the React app using `npm run build` and `npm start`.  
- **Backend:** Install dependencies from `requirements.txt` and start the Flask server.  
- **Admin View:** Install dependencies from `requirements.txt` and run the admin view with `python3 admin.py`.  
- **iOS App:** Update the WebView's URL to use the backend's IP address and port (8080) and recompile the app.

