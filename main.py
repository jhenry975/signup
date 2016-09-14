#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


form = """


    <form action="" method="post">
        <table>
            <tr>
                <td><h1>Signup</h1></td>
            </tr>
            <tr>
                <td><label>Username</label></td>
                <td>
                        <input name="username" type="text" value="%(username)s" required>
                            <span class="error">%(error_username)s</span>
                </td>
                </tr>
                    </br>
                    </br>
            <tr>
                <tr>
                <td><label>Password</label></td>
                <td>
                        <input name="password" type="text" value="" required>
                            <span class="error">%(error_password)s</span>
                </td>
            </tr>
                    </br>
                    </br>
            <tr>
                <td><label>Verify Password</label></td>
                <td>
                        <input name="verify" type="password" value="" required>
                            <span class="error">%(error_verify)s</span>
                </td>
            </tr>
                    </br>
                    </br>
            <tr>
                <td><label>Email</label></td>
                <td>
                        <input name="email" type="text" value="%(email)s">
                            <span class="error">%(error_email)s</span>
                </td>
            </tr>
        </table>
                    </br>
                    </br>
                    <input type="submit">
    </form>

"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S] + @[\S] + \.[\S] + $")
def valid_email(email):

    return not email and EMAIL_RE.match(email)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form %{"username":"", "email":"","error_username":"", "error_password":"", "error_verify":"", "error_email":""})

    def post(self):
        has_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email, error_username = "", error_password = "", error_verify = "", error_email = "")

        if not valid_username(username):
            params['error_username'] = "That is not a valid username"
            has_error = True

        if not valid_password(password):
            params['error_password'] = "That is not a valid password"
            has_error = True
        elif password != verify:
                params['error_verify'] = "Your passwords did not match"
                has_error = True

        if not valid_email(email):
            params['error_email'] = "That is not a valid email"
            has_error = True

        if has_error:
            self.response.out.write(form % params)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
