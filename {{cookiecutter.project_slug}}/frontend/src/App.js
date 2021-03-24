import React from "react";
import "fontsource-roboto";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import MomentUtils from "@date-io/moment";
import { AppLayout } from "euler-search-components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import AppMenu from "./AppMenu";
import { SearchPage, LoginPage } from "./pages";
import AuthService from "./components/auth";
import PrivateRoute from "./components/PrivateRoute";
import config from "./appConfig";
import {
  unstable_createMuiStrictModeTheme as createMuiTheme,
  ThemeProvider,
} from "@material-ui/core";

const theme = createMuiTheme();

const App = () => {
  const auth = new AuthService(config);
  return (
    <ThemeProvider theme={theme}>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <Router>
          <AppLayout title="{{ cookiecutter.project_name }}" menu={<AppMenu />}>
            <Switch>
              <Route exact path="/">
                <div>Home</div>
              </Route>
              <Route exact path="/login">
                <LoginPage
                  auth={auth}
                  title="{{ cookiecutter.project_name }} Login"
                />
              </Route>
              <PrivateRoute auth={auth} exact path="/search/:id">
                <SearchPage />
              </PrivateRoute>
            </Switch>
          </AppLayout>
        </Router>
      </MuiPickersUtilsProvider>
    </ThemeProvider>
  );
};

export default App;
