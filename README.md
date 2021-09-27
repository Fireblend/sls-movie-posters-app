# sls-movie-posters-app
A Serverless Flask WebApp, extracts dominant colors from movie posters.

Inspired by [pokepalettes](https://pokepalettes.com/)

## Running this:

#### 1. Setting up the lambda function.
Create a lambda function using Python 3.8 as its runtime.
Paste or upload the code from `lambda_function.py`. Add a valid TMDB API Key to the corresponding variable in the code.

Finally, add the following layer arns to its configuration:

* `arn:aws:lambda:us-east-1:668099181075:layer:AWSLambda-Python38-SciPy1x:29`
* `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-Pillow:13`
* `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-python38-requests:21`
* `arn:aws:lambda:us-east-1:446751924810:layer:python-3-8-scikit-learn-0-23-1:2`

Create a new API using API Gateway with a `get` method pointing to the function (enable `Lambda Proxy integration`). The function is set up to expect a `query` string parameter containing the movie title. Deploy it as part of a usage plan with an API Key. At this point you should be able to call the lambda through an API endpoint and get something like this in return. Use curl or postman to test:

```
'{"poster": "https://www.themoviedb.org/t/p/w500//7nO5DUMnGUuXrA4r2h6ESOKQRrx.jpg", 
  "primaryColor": "#6BA2D5", 
  "otherColors": [{"color": "#2B4282", "proportion": 0.41303306181121224}, 
                  {"color": "#96C0E5", "proportion": 0.16626736942980355}, 
                  {"color": "#C8D5E2", "proportion": 0.15572592237661714}, 
                  {"color": "#607291", "proportion": 0.1317680881648299}, 
                  {"color": "#2E2A31", "proportion": 0.06851940584571155}, 
                  {"color": "#BAAC93", "proportion": 0.06468615237182558}]}'
```

#### 2. Deploying the Serverless app.
For this part you'll need a Python 3.9 environment, or change the environment in the `serverless.yaml` file.

1. Install and set up the [AWS CLI](https://serverless.com/framework/docs/providers/aws/guide/credentials/) and [Serverless](https://serverless.com/framework/docs/providers/aws/guide/quick-start/) with your AWS credentials.
2. Set the `API_BASE_URL` and `API_KEY` environment variables with the right values from your API Gateway.
3. Install the required plugins in your cloned directory: `npm install --save serverless-wsgi serverless-python-requirements`
4. Execute `sls deploy`

And that should be it! The previous command should point you to the newly deployed application's URL.
