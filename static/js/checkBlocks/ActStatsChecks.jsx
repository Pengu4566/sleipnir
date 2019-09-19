import React from "react";
import ReactDOM from "react-dom";

export default class ActStatsChecks extends React.Component {
  render() {
    var data = this.props.name.file;
    return (
      <div
        className="checkbox-block"
        style={{ height: $(actStatsTable).height() }}
      >
        <div
          className="top-card d-flex align-items-center"
          id="actStatsChecksHeader"
        >
          <div className="ml-4" style={{ color: "white" }}>
            Please select file:
          </div>
        </div>
        <div className="content-box overflow-auto" style={{ height: "88.5%" }}>
          {data.map(file => (
            <React.Fragment key={file.index}>
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  defaultChecked
                  value={file.file}
                  id="defaultCheck1"
                />
                <label className="form-check-label">{file.file}</label>
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>
    );
  }
}
