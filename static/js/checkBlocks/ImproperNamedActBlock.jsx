import React from "react";

export default class ImproperNamedActBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>
              Activity naming is evaluated based on the activity type. No
              activity should be named with its default name.
            </p>
            <p>There is no improperly named activity.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[There is no activity in your project.]") {
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>There is no activity in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>
              Activity naming is evaluated based on the activity type. No
              activity should be named with its default name. Activities that
              are not properly named include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
