import axios from "axios";

const getEnv = (prop, envDefault) => {
  const env = process.env[prop];
  if (env !== undefined) {
    return env;
  } else {
    return envDefault;
  }
};

const baseApiURL = getEnv("REACT_APP_BASE_API_URL", "");

const config = {
  cookiePath: getEnv("REACT_APP_COOKIE_PATH", "/"),
  authURL: getEnv("REACT_APP_AUTH_URL", "/token"),
  loginURL: getEnv("REACT_APP_LOGIN_URL", "/login"),
  basePath: getEnv("REACT_APP_BASE_PATH", ""),
  baseApiURL: baseApiURL,
};

axios.defaults.baseURL = baseApiURL;
axios.defaults.withCredentials = true;
axios.defaults.headers.common["Accept"] = "application/json";

export default config;
