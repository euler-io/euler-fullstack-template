import React from "react";
import "fontsource-roboto";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import MomentUtils from "@date-io/moment";
import { AppLayout } from "euler-search-components";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import AppMenu from "./AppMenu";
import AuthMenu from "./components/AuthMenu";
import { SearchPage, LoginPage, NotFoundPage, DetailPage } from "./pages";
import AuthService from "./components/auth";
import PrivateRoute from "./components/PrivateRoute";
import config from "./appConfig";
import {
  unstable_createMuiStrictModeTheme as createMuiTheme,
  ThemeProvider,
} from "@material-ui/core";

const theme = createMuiTheme();

const App = () => {
  const history = useHistory();
  const auth = new AuthService(history, config);
  auth.init();
  return (
    <ThemeProvider theme={theme}>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <Router>
          <AppLayout
            title="{{cookiecutter.project_name}}"
            menu={<AppMenu />}
            leftMenu={
              <AuthMenu auth={auth} next={config.baseURL} login="/login" />
            }
          >
            <Switch>
              <Route exact path="/">
                <div>Home</div>
              </Route>
              <Route exact path="/login">
                <LoginPage auth={auth} title="Base Project Login" />
              </Route>
              <PrivateRoute auth={auth} exact path="/search/:searchId">
                <SearchPage />
              </PrivateRoute>
              <PrivateRoute auth={auth} exact path="/detail/:detailId/:id">
                <DetailPage />
              </PrivateRoute>
              <Route path="*">
                <NotFoundPage />
              </Route>
            </Switch>
          </AppLayout>
        </Router>
      </MuiPickersUtilsProvider>
    </ThemeProvider>
  );
};

export default App;
