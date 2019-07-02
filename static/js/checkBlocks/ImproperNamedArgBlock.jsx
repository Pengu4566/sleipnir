import React from "react";

export default class ImproperNamedArgBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>
              Argument naming is evaluated according to argument type, data
              type, and camel case rule.
            </p>
            <p>There is no improperly named argument.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[There is no argument in your project.]") {
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>There is no argument in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>
              Argument naming is evaluated according to argument type, data
              type, and camel case rule. Arguments that are not properly named
              include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
