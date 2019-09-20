import React from "react";

export default class Table1Filters extends React.Component {
  render() {
    var file = this.props.name.file;
    var type = this.props.name.type;
    var serror = this.props.name.error;
    var project = this.props.name.project;

    return (
      <React.Fragment>
        <div
          className="form-group has-search d-inline-block"
          style={{ width: "185px" }}
        >
          <span className="fa fa-search form-control-feedback"></span>
          <input
            type="text"
            className="form-control input-custom"
            placeholder="Search"
          />
        </div>
        <div className="dropdown d-inline ml-3">
          <button
            className="btn btn-primary extra-button-styles dropdown-toggle"
            style={{ verticalalign: "top" }}
            type="button"
            id="dropdownMenu2"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            File
          </button>
          <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
            {file.map(f => (
              <button
                className="dropdown-item"
                type="button"
                key={"file" + f.index}
              >
                {f.file}
              </button>
            ))}
          </div>
        </div>
        <div className="dropdown d-inline ml-3">
          <button
            className="btn btn-primary extra-button-styles dropdown-toggle"
            style={{ verticalalign: "top" }}
            type="button"
            id="dropdownMenu2"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            Type
          </button>
          <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
            {type.map(t => (
              <button
                className="dropdown-item"
                type="button"
                key={"type" + t.index}
              >
                {t.type}
              </button>
            ))}
          </div>
        </div>
        <div className="dropdown d-inline ml-3">
          <button
            className="btn btn-primary extra-button-styles dropdown-toggle"
            style={{ verticalalign: "top" }}
            type="button"
            id="dropdownMenu2"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            Error
          </button>
          <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
            {serror.map(e => (
              <button
                className="dropdown-item"
                type="button"
                key={"error" + e.index}
              >
                {e.error}
              </button>
            ))}
          </div>
        </div>
        <div className="dropdown d-inline ml-3">
          <button
            className="btn btn-primary extra-button-styles dropdown-toggle"
            style={{ verticalalign: "top" }}
            type="button"
            id="dropdownMenu2"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            Project
          </button>
          <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
            {project.map(p => (
              <button
                className="dropdown-item"
                type="button"
                key={"project" + p.index}
              >
                {p.project}
              </button>
            ))}
          </div>
        </div>
      </React.Fragment>
    );
  }
}
