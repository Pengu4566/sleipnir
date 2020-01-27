import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";
import styles from "../scss/adminPanel.scss";
import "../css/adminPanel.css";
import TenantTabs from "./components/tenentTabs";
import UserTabs from "./components/userTabs";

class AdminPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tenantExpand: true,
      userExpand: false
    };
    this.Logout = this.Logout.bind(this);
    this.ExpandElement = this.ExpandElement.bind(this);
    this.OnClickBack = this.OnClickBack.bind(this);
  }

  ExpandElement(e) {
    let name = e.target.id;
    this.setState({ [name]: !this.state[name] });
  }

  Logout() {
    window.location = "/logout";
  }

  OnClickBack(e) {
    window.location = "/upload";
  }

  render() {
    return (
      <React.Fragment>
        <div className="row justify-content-lg-center mt-5">
          <div className={classnames("col-lg-2")}></div>
          <div className={classnames("col-lg-8")}>
            <div className={classnames("main_div shadow-sm")}>
              <div
                className={classnames(
                  "justify-cotent-between",
                  "algin-self-center",
                  styles["header"]
                )}
              >
                <span className={classnames("ml-4", styles["header_text"])}>
                  Admin Panel
                </span>
                <span
                  className={classnames(
                    "mr-4",
                    styles["header_text"],
                    styles["username-cust"]
                  )}
                >
                  {username}&ensp;
                  <i
                    className={classnames(
                      "fa fa-sign-out",
                      styles["logout-cust"]
                    )}
                    onClick={() => this.Logout()}
                  ></i>
                </span>
              </div>
            </div>
            <div className={classnames("accordion")}>
              <div id="accordion">
                <div
                  className={classnames(
                    "card",
                    "rounded-0",
                    "bg-light",
                    styles["card-cust"]
                  )}
                >
                  <div
                    className={classnames(
                      "card-header",
                      "height_auto",
                      "border-0",
                      "rounded-0",
                      "pl-4",
                      styles["card-header-cust"]
                    )}
                  >
                    <h5
                      className={classnames(
                        "mb-2",
                        "heading-1",
                        "d-block",
                        styles["heading-1-cust"]
                      )}
                      id="tenantExpand"
                      onClick={e => this.ExpandElement(e)}
                    >
                      Tenant{" "}
                      {this.state.tenantExpand ? (
                        <i
                          id="tenantExpand"
                          className={classnames("fa fa-angle-up pl-3")}
                        ></i>
                      ) : (
                        <i
                          id="tenantExpand"
                          className={classnames("fa fa-angle-down pl-3")}
                        ></i>
                      )}
                    </h5>
                  </div>
                  <div
                    className={classnames("collapse")}
                    style={{
                      display: this.state.tenantExpand ? "block" : "none"
                    }}
                  >
                    <div
                      className={classnames(
                        "card-body",
                        "pl-4",
                        "pb-4",
                        styles["card-body-cust"],
                        styles["card-body-download-cust"]
                      )}
                    >
                      <TenantTabs />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className={classnames("accordion")}>
              <div id="accordion">
                <div
                  className={classnames(
                    "card",
                    "rounded-0",
                    "bg-light",
                    styles["card-cust"]
                  )}
                >
                  <div
                    className={classnames(
                      "card-header",
                      "height_auto",
                      "border-0",
                      "rounded-0",
                      "pl-4",
                      styles["card-header-cust"]
                    )}
                  >
                    <h5
                      className={classnames(
                        "mb-2",
                        "heading-1",
                        "d-block",
                        styles["heading-1-cust"]
                      )}
                      id="userExpand"
                      onClick={e => this.ExpandElement(e)}
                    >
                      User{" "}
                      {this.state.userExpand ? (
                        <i
                          id="userExpand"
                          className={classnames("fa fa-angle-up pl-3")}
                        ></i>
                      ) : (
                        <i
                          id="userExpand"
                          className={classnames("fa fa-angle-down pl-3")}
                        ></i>
                      )}
                    </h5>
                  </div>
                  <div
                    className={classnames("collapse")}
                    style={{
                      display: this.state.userExpand ? "block" : "none"
                    }}
                  >
                    <div
                      className={classnames(
                        "card-body",
                        "pl-4",
                        "pb-4",
                        styles["card-body-cust"],
                        styles["card-body-download-cust"]
                      )}
                    >
                      <UserTabs />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className={classnames("col-lg-2")}>
            <div className={classnames("row")}>
              <button
                className={classnames(styles["register-button-cust"])}
                onClick={e => this.OnClickBack(e)}
              >
                <i
                  className={classnames(
                    "fa fa-arrow-left",
                    styles["fa-gradiant"]
                  )}
                ></i>{" "}
                &nbsp;Back
              </button>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

ReactDOM.render(
  <AdminPanel username={username} user_id={user_id} />,
  document.getElementById("adminPanelContainer")
);
