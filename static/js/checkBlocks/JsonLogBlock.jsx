import React from "react";

export default class JsonLogBlock extends React.Component {
  render() {
    if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Project.Json Logging</h3>
          <div className="check_explain">
            <p>
              The project.json file should contain your own project name and
              description. Default values are not recommended.
            </p>
            <p>Project Name, Project Description: {this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
