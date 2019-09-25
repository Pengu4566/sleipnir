import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
<link
  rel="stylesheet"
  href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
></link>;

export default class Table1 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      nameText: "",
      fileText: "All Files",
      typeText: "All Types",
      errorText: "All Errors",
      projectText: "All Projects"
    };
  }
  render() {
    var data = JSON.parse(this.props.name.replace(/'/g, '"'));
    var file = data.file;
    var type = data.type;
    var serror = data.error;
    var project = data.project;
    var data = data.data;

    if (this.state.nameText != "") {
      data = data.filter(d => {
        return d.name
          .toLowerCase()
          .match(".*" + this.state.nameText.toLowerCase() + ".*");
      });
    }
    if (this.state.fileText != "All Files") {
      data = data.filter(d => {
        return d.file.match(this.state.fileText);
      });
    }
    if (this.state.typeText != "All Types") {
      data = data.filter(d => {
        return d.type.match(this.state.typeText);
      });
    }
    if (this.state.errorText != "All Errors") {
      data = data.filter(d => {
        return d.error.match(this.state.errorText);
      });
    }
    if (this.state.projectText != "All Projects") {
      data = data.filter(d => {
        return d.project.match(this.state.projectText);
      });
    }

    const columns = [
      {
        Header: "id",
        accessor: "index",
        id: "index",
        show: false
      },
      {
        Header: "Name",
        accessor: "name"
      },
      {
        Header: "File",
        accessor: "file"
      },
      {
        Header: "Type",
        accessor: "type"
      },
      {
        Header: "Error",
        accessor: "error"
      },
      {
        Header: "Project",
        accessor: "project"
      }
    ];

    return (
      <React.Fragment>
        <div className="row justify-content-lg-left">
          <div className="col-lg-12">
            <div className="ml-4 mt-4 mb-4">
              <span className="heading-1 d-block">
                Project Compliance Backlog
              </span>
            </div>
            <div className="ml-4 mt-4 mb-4" id="table1Filters">
              <div
                className="form-group has-search d-inline-block"
                style={{ width: "185px" }}
              >
                <span className="fa fa-search form-control-feedback"></span>
                <input
                  type="text"
                  className="form-control input-custom"
                  placeholder="Name Search"
                  id="t1NameFilter"
                  onChange={() =>
                    this.setState({ nameText: event.target.value })
                  }
                />
              </div>
              <div className="dropdown d-inline ml-3">
                <button
                  className="btn btn-primary extra-button-styles dropdown-toggle"
                  style={{ verticalalign: "top" }}
                  type="button"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  id="t1FileFilter"
                >
                  {this.state.fileText}
                </button>

                <div
                  className="dropdown-menu"
                  aria-labelledby="dropdownMenu2"
                  id="fileDropdownMenu"
                >
                  {file.map(f => (
                    <li
                      className="dropdown-item"
                      key={"t1file" + f.index}
                      onClick={() =>
                        this.setState({ fileText: event.target.innerText })
                      }
                    >
                      {f.file}
                    </li>
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
                  id="t1TypeFilter"
                >
                  {this.state.typeText}
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {type.map(t => (
                    <li
                      className="dropdown-item"
                      key={"t1type" + t.index}
                      onClick={() =>
                        this.setState({ typeText: event.target.innerText })
                      }
                    >
                      {t.type}
                    </li>
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
                  id="t1ErrorFilter"
                >
                  {this.state.errorText}
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {serror.map(e => (
                    <li
                      className="dropdown-item"
                      key={"t1error" + e.index}
                      onClick={() =>
                        this.setState({ errorText: event.target.innerText })
                      }
                    >
                      {e.error}
                    </li>
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
                  id="t1ProjectFilter"
                >
                  {this.state.projectText}
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {project.map(p => (
                    <li
                      className="dropdown-item"
                      key={"t1project" + p.index}
                      onClick={() =>
                        this.setState({ projectText: event.target.innerText })
                      }
                    >
                      {p.project}
                    </li>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="col-lg-12">
              <ReactTable
                className="table table_fixed ml-2 mr-2"
                columns={columns}
                data={data}
                defaultPageSize={10}
                showPageSizeOptions={false}
              />
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}
