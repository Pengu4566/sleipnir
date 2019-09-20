import React from "react";

export default class CheckButtons extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapseNaming: false,
      collapseUsage: false,
      collapseDoc: false
    };
  }
  toggleNaming() {
    this.setState(state => ({ collapseNaming: !state.collapseNaming }));
  }
  toggleUsage() {
    this.setState(state => ({ collapseUsage: !state.collapseUsage }));
  }
  toggleDoc() {
    this.setState(state => ({ collapseDoc: !state.collapseDoc }));
  }

  render() {
    return (
      <div id="all_categories">
        <button
          className="categories_btn"
          id="namingCat"
          onClick={this.toggleNaming.bind(this)}
        >
          Naming
        </button>
        <div
          className="checklist"
          style={{ display: this.state.collapseNaming ? "none" : "block" }}
        >
          <p>Score: {this.props.naming}</p>
          <p>Check List</p>
          <ul>
            <li>Variable Naming</li>
            <li>Argument Naming</li>
            <li>Activity Naming</li>
          </ul>
        </div>
        <button
          className="categories_btn"
          id="usageCat"
          onClick={this.toggleUsage.bind(this)}
        >
          Usage
        </button>
        <div
          className="checklist"
          style={{ display: this.state.collapseUsage ? "none" : "block" }}
        >
          <p>Score: {this.props.usage}</p>
          <p>Check List</p>
          <ul>
            <li>Variable Usage</li>
            <li>Argument Usage</li>
          </ul>
        </div>

        <button
          className="categories_btn"
          id="documentationCat"
          onClick={this.toggleDoc.bind(this)}
        >
          Documentation
        </button>
        <div
          className="checklist"
          style={{ display: this.state.collapseDoc ? "none" : "block" }}
        >
          <p>Score: {this.props.doc}</p>
          <p>Check List</p>
          <ul>
            <li>Workflow Annotation</li>
            <li>Try Catch Logging</li>
            <li>Try Catch Screenshot</li>
            <li>Project.Json Logging</li>
            <li>Argument Explanation in Annotation</li>
          </ul>
        </div>
      </div>
    );
  }
}
