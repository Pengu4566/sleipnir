import React from "react";

export default class UnusedArgBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Argument Usage</h3>
          <div className="check_explain">
            <p>
              Argument usage is evaluate based on how many arguments are
              declared but not used.
            </p>
            <p>There is no unused argument.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else if (this.props.name == "[There is no argument in your project.]") {
      return (
        <div className="single_check">
          <h3>Argument Usage</h3>
          <div className="check_explain">
            <p>There is no argument in your project.</p>
          </div>
        </div>
      );
    } else {
      return (
        <div className="single_check">
          <h3>Argument Usage</h3>
          <div className="check_explain">
            <p>
              Argument usage is evaluate based on how many arguments are
              declared but not used. An unused argument should be deleted. Such
              arguments include:
            </p>
            <p> {this.props.name} </p>
          </div>
        </div>
      );
    }
  }
}
