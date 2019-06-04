import React from "react";

export default class ImproperNamedActBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no improperly named activity.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else if (this.props.name == "[There is no activity in your project.]") {
      return (
        <div>
          <p>There is no activity in your project.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <p>
            {" "}
            An activity should not use its default name. Activities that are not
            properly named include:{" "}
          </p>
          <p>{this.props.name}</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    }
  }
}
