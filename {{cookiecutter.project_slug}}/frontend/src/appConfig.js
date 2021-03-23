import axios from "axios";

const getEnv = (prop, envDefault) => {
  const env = process.env[prop];
  if (env !== undefined) {
    return env;
  } else {
    return envDefault;
  }
};

const getUrl = (url, baseURL) => {
  if (/^https?/.test(url)) {
    return url;
  } else {
    return `${baseURL}${url}`;
  }
};

const baseApiURL = getEnv("REACT_APP_BASE_API_URL", "");
const baseURL = getEnv("REACT_APP_BASE_URL", "");
const authURL = getEnv("REACT_APP_AUTH_URL", "/token");
const loginURL = getEnv("REACT_APP_LOGIN_URL", "/login");

const config = {
  baseApiURL: baseApiURL,
  authURL: getUrl(authURL, baseApiURL),
  baseURL: baseURL,
  loginURL: getUrl(loginURL, baseURL),
  cookiePath: getEnv("REACT_APP_COOKIE_PATH", "/"),
};

axios.defaults.baseURL = baseApiURL;
axios.defaults.withCredentials = true;
axios.defaults.headers.common["Accept"] = "application/json";

export default config;
