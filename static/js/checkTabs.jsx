import React from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";
import "react-toggle/style.css";
import classnames from "classnames";
import styles from "../scss/check_tabs.scss";
import Toggle from "react-toggle";

export default class CheckTabs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
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
    };
  }
  onToggleChange(e) {
    this.setState({ [e.target.id]: !this.state[e.target.id] }, e => {
      this.props.getSetting(this.state);
    });
  }
  render() {
    return (
      <Tabs>
        <TabList>
          <Tab>Name</Tab>
          <Tab>Usage</Tab>
          <Tab>Documentation</Tab>
        </TabList>

        <TabPanel>
          <div className="clearfix pt-4 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Variable Naming
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                id="varName"
                name="VariableNaming"
                value="VariableNaming"
                onChange={e => this.onToggleChange(e)}
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Argument Naming
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                id="argName"
                onChange={e => this.onToggleChange(e)}
                name="ArgumentNaming"
                value="ArgumentNaming"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 pb-4 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Activity Naming
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                id="actName"
                name="ActivityNaming"
                value="ActivityNaming"
                defaultChecked
              />
            </label>
          </div>
        </TabPanel>
        <TabPanel>
          <div className="clearfix pt-4 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Variable Usage
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="VariableUsage"
                value="VariableUsage"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 pb-4 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Argument Usage
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="ArgumentUsage"
                value="ArgumentUsage"
                defaultChecked
              />
            </label>
          </div>
        </TabPanel>
        <TabPanel>
          <div className="clearfix pt-4 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Workflow Annotation
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="WorkflowAnnotation"
                value="WorkflowAnnotation"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Try Catch Logging
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="TryCatchLogging"
                value="TryCatchLogging"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Try Catch Screenshot
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="TryCatchScreenshot"
                value="TryCatchScreenshot"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Project.Json Logging
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="JsonLogging"
                value="JsonLogging"
                defaultChecked
              />
            </label>
          </div>
          <div className="clearfix mt-3 ml-5 mr-5 pb-4 d-block">
            <label className={classnames("d-block")}>
              <span
                className={classnames(
                  "float-left",
                  styles["toggle-label-cust"]
                )}
              >
                Argument Explanation in Annotation
              </span>
              <Toggle
                className={classnames("float-right", styles["toggle-cust"])}
                onChange={e => this.onToggleChange(e)}
                name="ArgExpAnnot"
                value="ArgExpAnnot"
                defaultChecked
              />
            </label>
          </div>
        </TabPanel>
      </Tabs>
    );
  }
}
