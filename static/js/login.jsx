import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";
import styles from "../scss/login_page.scss";

class LoginWindow extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tenant: "",
      username: "",
      password: ""
    };
    this.updateState = this.updateState.bind(this);
    this.login = this.login.bind(this);
  }

  updateState(e) {
    let name = e.target.name;
    let value = e.target.value;

    this.setState({ [name]: value });
  }

  login(e) {
    if (
      this.state.tenant != "" &&
      this.state.username != "" &&
      this.state.password != ""
    ) {
      $.ajax({
        url: "/login",
        type: "POST",
        data: JSON.stringify(this.state),
        contentType: "json/application",
        dataType: "json",
        success: function(response) {
          window.location = "/upload";
        },
        error: function(e) {
          window.alert(e.responseJSON.message);
        }
      });
    } else {
      alert("Please fill in all required fields.");
    }
  }

  render() {
    return (
      <React.Fragment>
        <div className={classnames("row")}>
          <div className="col-sm-4"></div>
          <div className="col-sm-4">
            <div className={classnames(styles["login-header-cust"])}>
              <h3>AKOA Code Testing App Login</h3>
            </div>
            <div className={classnames("row", styles["tenant-cust"])}>
              <label className={classnames(styles["label-cust"])}>Tenant</label>
              <input
                type="text"
                name="tenant"
                onChange={e => this.updateState(e)}
                className={classnames(styles["input-cust"])}
              />
            </div>
            <div className={classnames("row", styles["username-cust"])}>
              <label className={classnames(styles["label-cust"])}>
                Username
              </label>
              <input
                type="text"
                name="username"
                onChange={e => this.updateState(e)}
                className={classnames(styles["input-cust"])}
              />
            </div>
            <div className={classnames("row", styles["password-cust"])}>
              <label className={classnames(styles["label-cust"])}>
                Password
              </label>
              <input
                type="password"
                name="password"
                onChange={e => this.updateState(e)}
                className={classnames(styles["input-cust"])}
              />
            </div>
            <div className={classnames("row", styles["login-cust"])}>
              <button
                className={classnames(styles["login-button-cust"])}
                onClick={e => this.login(e)}
              >
                Login
              </button>
            </div>
          </div>
          <div className="col-sm-4"></div>
        </div>
      </React.Fragment>
    );
  }
}

ReactDOM.render(<LoginWindow />, document.getElementById("loginContainer"));
