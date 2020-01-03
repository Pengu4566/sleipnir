import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";
import "../css/checkTabs.css";
import styles from "../scss/landing_page.scss";
import CheckTabs from "./checkTabs";
import Spinner from "react-bootstrap/Spinner";
import Loader from "react-loader-spinner";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";

class FileUploader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      settingExpand: true,
      downloadExpand: false,
      setting: {
        varName: true,
        argName: true,
        actName: true,
        varUsage: true,
        argUsage: true,
        wfAnnot: true,
        tcLog: true,
        tcSs: true,
        jsonLog: true,
        argExp: true
      },
      fileName: "",
      uploading: false,
      analyzing: false,
      filePath: ""
    };
    this.ExpandSetting = this.ExpandSetting.bind(this);
    this.ExpandDownload = this.ExpandDownload.bind(this);
    this.OnChooseFile = this.OnChooseFile.bind(this);
    this.GetSetting = this.GetSetting.bind(this);
    this.OnUpload = this.OnUpload.bind(this);
    this.logout = this.logout.bind(this);
  }

  ExpandSetting() {
    this.setState({ settingExpand: !this.state.settingExpand });
  }

  ExpandDownload() {
    this.setState({ downloadExpand: !this.state.downloadExpand });
  }

  GetSetting(childState) {
    this.setState({ setting: childState });
  }

  logout() {
    window.location = "/logout";
  }

  OnChooseFile(e) {
    e.preventDefault();
    if (this.state.filePath != "") {
    }
    let files = e.target.files[0];
    let filePath = e.target.files[0].name;
    var form_data = new FormData();
    if (
      filePath.toLowerCase().endsWith(".zip") &&
      filePath.replace(".", "").length == filePath.length - 1
    ) {
      this.setState(
        {
          fileName: filePath,
          uploading: true
        },
        () => {
          form_data.append("file", files);
          $.ajax({
            url: "/fileUploading",
            type: "POST",
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(e) {},
            error: function(e) {
              alert("File Error. Please upload a valid zip file.");
            }
          }).then(response => {
            this.setState({
              filePath: response.fileLocation,
              uploading: false
            });
          });
          // .catch(error => {
          //   alert("File Error. Please upload a valid zip file.");
          // });
        }
      );
    } else {
      window.alert("Please choose a zip file with project(s) zipped inside.");
    }
  }

  OnUpload(e) {
    e.preventDefault();
    if (this.state.filePath == "") {
      window.alert("Please choose a zip file to upload first.");
    } else {
      this.setState({ analyzing: true }, () => {
        $.ajax({
          url: "/processing",
          type: "POST",
          data: JSON.stringify(this.state),
          contentType: "json/application",
          dataType: "json",
          success: function(response) {
            window.location = "/result";
          },
          error: function(e) {
            window.alert("Failed to analyze. Please upload a valid zip file.");
          }
        });
      });
    }
  }

  render() {
    return (
      <React.Fragment>
        <div className="row justify-content-lg-center mt-5">
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
                  Code Review App
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
                    onClick={() => this.logout()}
                  ></i>
                </span>
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
                      <h5 className={classnames("mb-2")}>
                        <button
                          className={classnames(
                            "btn",
                            "heading-1",
                            "d-block",
                            styles["heading-1-cust"]
                          )}
                          type="button"
                          onClick={() => this.ExpandSetting()}
                        >
                          Step 1 - Settings{" "}
                          <span className={classnames("pl-3")}>
                            {this.state.settingExpand ? (
                              <i className={classnames("fa fa-angle-up")}></i>
                            ) : (
                              <i className={classnames("fa fa-angle-down")}></i>
                            )}
                          </span>
                        </button>
                        <span className={classnames(styles["heading-2"])}>
                          Please customize the your checks
                        </span>
                      </h5>
                    </div>
                    <div
                      className={classnames("collapse")}
                      style={{
                        display: this.state.settingExpand ? "block" : "none"
                      }}
                    >
                      <div
                        className={classnames(
                          "card-body",
                          "pb-4",
                          styles["card-body-cust"],
                          styles["card-body-download-cust"]
                        )}
                      >
                        <CheckTabs getSetting={this.GetSetting} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div
                className={classnames(
                  "card rounded-0 bg-light border-top-none border-bottom-none"
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
                  <h5 className={classnames("mb-3", "mt-2", "d-inline-block")}>
                    <div
                      className={classnames(
                        "heading-1",
                        "d-block",
                        "pb-2",
                        styles["heading-1-cust"]
                      )}
                    >
                      Step 2 - Choose File
                    </div>
                    <span className={classnames(styles["heading-2"])}>
                      {this.state.fileName == ""
                        ? "Please upload the file in .zip format"
                        : "File Chosen: " + this.state.fileName}
                    </span>
                  </h5>
                  <label
                    className={
                      this.state.analyzing
                        ? classnames(
                            "btn btn-primary ml-0 mt-2 pt-2 pb-2 pl-3 pr-3",
                            styles["btn-primary-cust"],
                            styles["upload-button-cust"],
                            styles["upload-button-disable-cust"]
                          )
                        : classnames(
                            "btn btn-primary ml-0 mt-2 pt-2 pb-2 pl-3 pr-3",
                            styles["btn-primary-cust"],
                            styles["upload-button-cust"]
                          )
                    }
                  >
                    {this.state.uploading ? (
                      <span
                        className={classnames(
                          "btn_text pl-1",
                          styles["upload-span-cust"]
                        )}
                      >
                        <Spinner animation="border" variant="light" size="sm" />
                        {"  "}Uploading ...
                      </span>
                    ) : (
                      <span
                        className={
                          (classnames("btn_text pl-1"),
                          styles["upload-span-cust"])
                        }
                      >
                        <i className={classnames("fa fa-upload")}></i>
                        {"  "} Choose File
                      </span>
                    )}
                    <input
                      type="file"
                      name="file"
                      id="file"
                      onChange={e => this.OnChooseFile(e)}
                      hidden
                      disabled={this.state.uploading || this.state.analyzing}
                    ></input>
                  </label>
                </div>
              </div>

              <div className={classnames("card rounded-0 border-top-none")}>
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
                  <h5 className={classnames(styles["mb-0"])}>
                    <div
                      className={classnames(
                        "heading-1",
                        "d-block",
                        "pb-2",
                        styles["heading-1-cust"]
                      )}
                    >
                      Step 3 - Press &amp; Go
                    </div>
                  </h5>
                  <div className={classnames("d-flex justify-content-center")}>
                    <button
                      id="uploadText"
                      onClick={e => this.OnUpload(e)}
                      className={classnames(
                        "d-flex justify-content-center btn btn-primary pt-2 pb-2 pr-0",
                        styles["btn-primary-cust"]
                      )}
                      style={{ width: "100%" }}
                      disabled={
                        this.state.filePath == "" || this.state.analyzing
                      }
                    >
                      <span className={classnames("d-flex btn_text")}>
                        <div id="Progress">Analyze</div>
                      </span>
                    </button>
                    {/* <script type="text/javascript">
                      $("#fileUploadForm").submit(function () {
                        $("#uploadText").attr("disabled", true);
                      });
                      $(document).ready(function () {
                        var socket = io({ transports: ['websocket'] });
                        socket.on('progress', function (msg) {
                          console.log(msg.data);
                          $('#Progress').html('<p style="margin: 0%;">' + msg.data + '</p>');
                        });
                      });
                    </script> */}
                  </div>
                </div>
              </div>

              <div className={classnames("accordion1")}>
                <div id="accordion1">
                  <div
                    className={classnames(
                      "card rounded-0 bg-light mb-5",
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
                      id="headingOne"
                      style={{ backgroundColor: "white" }}
                    >
                      <h5 className={classnames(styles["mb-2"])}>
                        <button
                          className={classnames(
                            "btn",
                            "heading-1",
                            "d-block",
                            styles["heading-1-cust"]
                          )}
                          type="button"
                          onClick={() => this.ExpandDownload()}
                        >
                          AKOA Template Download{" "}
                          <span className={classnames("pl-3")}>
                            {this.state.downloadExpand ? (
                              <i className={classnames("fa fa-angle-up")}></i>
                            ) : (
                              <i className={classnames("fa fa-angle-down")}></i>
                            )}
                          </span>
                        </button>
                      </h5>
                    </div>
                    <div
                      className={classnames(
                        "card-body",
                        styles["card-body-cust"]
                      )}
                      style={{
                        display: this.state.downloadExpand ? "block" : "none"
                      }}
                    >
                      <div
                        className={classnames(
                          "heading-1 d-block mb-2 mt-2",
                          styles["download-text-cust"]
                        )}
                      >
                        Queue Template{" "}
                        <a href="/download/queue" target="blank">
                          <i className={classnames("fa fa-download ml-3")}></i>
                        </a>
                      </div>
                      <div
                        className={classnames(
                          "heading-1 d-block mb-2 mt-2",
                          styles["download-text-cust"]
                        )}
                      >
                        Non-Queue Template
                        <a href="/download/nonqueue" target="blank">
                          <i className={classnames("fa fa-download ml-3")}></i>
                        </a>
                      </div>
                      <div
                        className={classnames(
                          "heading-1 d-block mb-2 mt-2",
                          styles["download-text-cust"]
                        )}
                      >
                        Non-Repetitive Template
                        <a href="/download/nonrepetitive" target="blank">
                          <i className={classnames("fa fa-download ml-3")}></i>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

ReactDOM.render(
  <FileUploader username={username} user_id={user_id} />,
  document.getElementById("fileUploadContainer")
);
