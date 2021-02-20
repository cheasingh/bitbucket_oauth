# bitbucket_oauth

Generate pullrequest from bitbucket using OAuth2, automatically do a token behave on user behalf.

### Prerequisite

Provide a custom `Rauth` python package that work with bitbucket refresh token.
To get start, clone this repository. and create an empty folder for `token`.
Create a `.env` file to store bitbucket `client_id` and `client_secret`.

1. go to bitbucket to create consumer app [bitbucket](https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/)
2. install prerequisite - `pip -r install requirements`
3. run `main.py`, for the very first time, it will display an token authenticate link in the console.
4. copy the link, paste it in browser and copy the redirect url. **url** contain authentication code.
5. paste the url back in the console.
