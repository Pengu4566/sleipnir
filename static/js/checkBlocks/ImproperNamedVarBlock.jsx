import React from "react";

export default class ImproperNamedVarBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Variable Naming</h3>
          <div className="check_explain">
            <p>
              Variable naming is evaluated according to camel case rule and the
              variable's data type.
            </p>
            <p>
              According to our best practice, there is no improperly named
              variable.
            </p>
          </div>
        </div>
      );
    } else if (this.props.name == "[There is no variable in your project.]") {
      return (
        <div className="single_check">
          <h3>Variable Naming</h3>
          <div className="check_explain">
            <p>There is no variable in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Variable Naming</h3>
          <div className="check_explain">
            <p>
              Variable naming is evaluated according to camel case rule and the
              variable's data type. Variables that are not properly named
              include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
