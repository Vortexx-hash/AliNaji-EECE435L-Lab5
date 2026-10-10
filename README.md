# Lab 5 Flask user app

The Flask API in `app.py` calls the existing functions in `database.py`.
The database code and the existing `database.db` are preserved. The app creates
the users table automatically if needed.

## Run the server

Open a PowerShell terminal in this repository. The `venv` has already been created
and its dependencies installed on this computer.

```powershell
.\venv\Scripts\python.exe app.py
```

Keep that terminal running while using Postman. The server URL is
`http://127.0.0.1:5000`. Run from this repository because the existing database
module opens `database.db` relative to the current directory.

To activate the environment explicitly:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

If PowerShell blocks activation, use the first command with the full Python path;
activation is optional and no execution-policy change is needed.

On a teammate's computer, create and install the environment first:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

Python includes `sqlite3`. `db-sqlite3` is also installed to follow the handout;
the database functions use Python's built-in module. CORS is enabled as requested.

## Exact Postman steps

1. Open Postman desktop and enter a workspace.
2. Click **Import** and import both files from `postman/`:
   `Flask user app.postman_collection.json` and
   `Lab5 Local.postman_environment.json`.
3. Check that the collection is named **Flask user app**.
4. Select **Lab5 Local** in the environment selector at the top right.
5. In that environment, verify `base_url` is `http://127.0.0.1:5000` with no
   trailing slash. Leave `user_id` empty initially.
6. Open the collection and send its requests in the numbered order below.
   For requests with a body, **Body > raw > JSON** is already configured, and
   `Content-Type: application/json` is already included. No authorization is needed.
7. After each request, check the response status, JSON body, and **Test Results**.
   The tests run automatically from **Scripts > Post-response**.
8. For the graded examples, click **Save Response > Save as example** after each
   actual request and give it a descriptive name. The imported examples are
   illustrative fixtures; save your own actual responses for the submission.
9. Export the collection and environment after testing, and capture screenshots
   of the responses, passing tests, environment variables, and saved examples if
   your instructor asks for evidence. Do not remove the `{{base_url}}` references.

The POST test automatically stores the returned ID in the environment's
`user_id`. Use that ID throughout; do not assume it will always be 1.
If manually recreating the requests, copy the POST response's `user_id` into
the environment before continuing.

You can also choose **Run collection**, select **Lab5 Local**, keep requests
01–08 in order, and run one iteration. All 24 assertions should pass.
Send requests individually afterward to save your actual response examples.

| Order | Method | URL | Expected response |
| --- | --- | --- | --- |
| 01 List users | GET | `{{base_url}}/api/users` | 200, JSON array; initially `[]` if the database is empty |
| 02 Add user | POST | `{{base_url}}/api/users/add` | 200, John Doe object with a generated numeric `user_id` |
| 03 Get added user | GET | `{{base_url}}/api/users/{{user_id}}` | 200, the same John Doe record |
| 04 Update user | PUT | `{{base_url}}/api/users/update` | 200, Jane Doe record with the same ID |
| 05 Verify update | GET | `{{base_url}}/api/users/{{user_id}}` | 200, saved Jane Doe values |
| 06 Delete user | DELETE | `{{base_url}}/api/users/delete/{{user_id}}` | 200, `{"status":"User deleted successfully"}` |
| 07 Verify deletion | GET | `{{base_url}}/api/users/{{user_id}}` | 404, `{"error":"User not found"}`; this is a passing test |
| 08 List after deletion | GET | `{{base_url}}/api/users` | 200, array without the deleted user's ID; `[]` if there are no other users |

### POST body for request 02

```json
{
  "name": "John Doe",
  "email": "johndoe@gmail.com",
  "phone": "067765434567",
  "address": "John Doe Street, Innsbruck",
  "country": "Austria"
}
```

Do not send `user_id` when adding a user. The database generates it.

### PUT body for request 04

Paste this into **Body > raw > JSON** in Postman. Postman replaces `{{user_id}}`
with the numeric environment value before sending the body. Leave it unquoted.

```text
{
  "user_id": {{user_id}},
  "name": "Jane Doe",
  "email": "janedoe@gmail.com",
  "phone": "067765434567",
  "address": "John Doe Street, Innsbruck",
  "country": "Austria"
}
```

All five text fields are required for both POST and PUT. `phone` must stay a
string so its leading zero is preserved. PUT also requires a positive integer ID.
Successful requests use 200, matching the handout. Missing users return 404
instead of the handout's empty object, and invalid JSON or fields return 400.
Sending a body without JSON content type returns 415.

### Browser GET checks

While the server is running, open `http://127.0.0.1:5000/api/users` in your browser.
After adding a user, also open `http://127.0.0.1:5000/api/users/<actual ID>`.
The `/` page has no endpoint and will return 404; use the API URLs above.

### Troubleshooting

- Connection refused: keep the Flask terminal running and verify `base_url`.
- Undefined variables: select **Lab5 Local**, then send request 02 before 03–07.
- 400 on PUT: ensure all fields are included and `user_id` is numeric, not quoted.
- 415: select **Body > raw > JSON**, not Text or form-data.
- 404 after deleting: expected for request 07. To restart the sequence, run 01–08
  again so POST creates a fresh record and saves its ID.
- Use the desktop app for localhost. The web app's cloud agent cannot reach
  this local server; the web app requires the Postman Desktop Agent.

## Automated verification

```powershell
.\venv\Scripts\python.exe -m unittest -v test_api
```

The tests cover the complete CRUD lifecycle, validation, missing users, JSON
errors, HTTP methods, CORS preflight, database write failure responses, and the
teammate's original database tests. All test data is stored in temporary
databases, leaving the repository database unchanged.

To execute the exported collection from a terminal while the server is running
(requires Node.js and downloads Newman into the npm cache):

```powershell
npx.cmd --yes newman run "postman/Flask user app.postman_collection.json" -e "postman/Lab5 Local.postman_environment.json"
```

## References

- [Flask quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Postman quick start](https://learning.postman.com/docs/getting-started/quick-start/)
- [Postman requests](https://learning.postman.com/docs/use/send-requests/requests/)
- [Postman environments](https://learning.postman.com/docs/use/send-requests/variables/managing-environments/)
- [Postman response examples](https://learning.postman.com/docs/use/send-requests/response-data/examples/)
