import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";
import styles from "../scss/landing_page.scss";

class FileUploader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      settingExpand: true,
      downloadExpand: false
    };
    this.ExpandSetting = this.ExpandSetting.bind(this);
    this.ExpandDownload = this.ExpandDownload.bind(this);
  }

  ExpandSetting() {
    this.setState({ settingExpand: !this.state.settingExpand });
  }

  ExpandDownload() {
    this.setState({ downloadExpand: !this.state.downloadExpand });
  }

  render() {
    return (
      <React.Fragment>
        <div className="row justify-content-lg-center mt-5">
          <div className={classnames("col-lg-8")}>
            <div className={classnames("main_div shadow-sm")}>
              <div className={classnames("d-flex", styles["header"])}>
                <div className={classnames("d-flex", "align-self-center")}>
                  <span className={classnames("ml-4", styles["header_text"])}>
                    Code Review App
                  </span>
                </div>
              </div>
              <form
                action="uploader"
                method="post"
                encType="multipart/form-data"
                id="fileUploadForm"
              >
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
                                <i
                                  className={classnames("fa fa-angle-down")}
                                ></i>
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
                          <div
                            className={classnames(
                              "row justify-content-lg-center pl-2"
                            )}
                          >
                            <div className={classnames("col-lg-4")}>
                              <div
                                className={classnames(styles["check_boxes"])}
                              >
                                <span
                                  className={classnames(
                                    "d-block mb-2",
                                    styles["category-cust"]
                                  )}
                                >
                                  Naming
                                </span>
                                <div className={classnames("form-check")}>
                                  <input
                                    className={classnames("form-check-input")}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="VariableNaming"
                                    value="VariableNaming"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Variable Naming
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="ArgumentNaming"
                                    value="ArgumentNaming"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Argument Naming
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="ActivityNaming"
                                    value="ActivityNaming"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Activity Naming
                                  </label>
                                </div>
                              </div>
                            </div>

                            <div
                              className={classnames(styles["col-lg-4"])}
                              style={{ paddingLeft: "30px" }}
                            >
                              <div
                                className={classnames(styles["check_boxes"])}
                              >
                                <span
                                  className={classnames(
                                    "d-block mb-2",
                                    styles["category-cust"]
                                  )}
                                >
                                  Usage
                                </span>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="VariableUsage"
                                    value="VariableUsage"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Variable Usage
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="ArgumentUsage"
                                    value="ArgumentUsage"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Argument Usage
                                  </label>
                                </div>
                              </div>
                            </div>

                            <div
                              className={classnames(styles["col-lg-4"])}
                              style={{ paddingLeft: "30px" }}
                            >
                              <div
                                className={classnames(styles["check_boxes"])}
                              >
                                <span
                                  className={classnames(
                                    "d-block mb-2",
                                    styles["category-cust"]
                                  )}
                                >
                                  Documentation
                                </span>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="WorkflowAnnotation"
                                    value="WorkflowAnnotation"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Workflow Annotation
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="TryCatchLogging"
                                    value="TryCatchLogging"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Try Catch Logging
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="TryCatchScreenshot"
                                    value="TryCatchScreenshot"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Try Catch Screenshot
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="JsonLogging"
                                    value="JsonLogging"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Project.Json Logging
                                  </label>
                                </div>

                                <div
                                  className={classnames(styles["form-check"])}
                                >
                                  <input
                                    className={classnames(
                                      styles["form-check-input"]
                                    )}
                                    type="checkbox"
                                    id="defaultCheck1"
                                    name="ArgExpAnnot"
                                    value="ArgExpAnnot"
                                    defaultChecked
                                  ></input>
                                  <label
                                    className={classnames(
                                      styles["form-check-label"]
                                    )}
                                    htmlFor="defaultCheck1"
                                  >
                                    Argument Explanation in Annotation
                                  </label>
                                </div>
                              </div>
                            </div>
                          </div>
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
                    <h5
                      className={classnames("mb-3", "mt-2", "d-inline-block")}
                    >
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
                        Please upload the file in .zip format
                      </span>
                    </h5>
                    <label
                      className={classnames(
                        "btn btn-primary ml-0 mt-2 pt-2 pb-2 pl-3 pr-3",
                        styles["btn-primary-cust"],
                        styles["upload-button-cust"]
                      )}
                    >
                      <span className={classnames("btn_text pl-1")}>
                        <i className={classnames("fa fa-upload")}></i>
                        &nbsp;&nbsp; Choose File
                      </span>
                      <input type="file" name="file" id="file" hidden></input>
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
                    <div
                      className={classnames("d-flex justify-content-center")}
                    >
                      <button
                        id="uploadText"
                        className={classnames(
                          "d-flex justify-content-center btn btn-primary pt-2 pb-2 pr-0",
                          styles["btn-primary-cust"]
                        )}
                        style={{ width: "100%" }}
                      >
                        <input
                          type="submit"
                          value="Upload"
                          className={classnames(styles["submitBtn"])}
                          hidden
                        ></input>
                        <span className={classnames("d-flex btn_text")}>
                          <div id="Progress">Upload</div>
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
              </form>

              <div className={classnames(styles["accordion1"])}>
                <div id="accordion1">
                  <div
                    className={classnames(
                      "card rounded-0 bg-light mb-3",
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
  <FileUploader />,
  document.getElementById("fileUploadContainer")
);
