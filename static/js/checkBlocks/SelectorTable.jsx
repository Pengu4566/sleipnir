import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class SelectorTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectorText: "",
      fileText: "All Files",
      projectText: "All Projects"
    };
  }
  render() {
    var data = JSON.parse(this.props.name.replace(/'/g, '"'));
    var file = data.file;
    var project = data.project;
    var data = data.data;

    if (this.state.selectorText != "") {
      data = data.filter(d => {
        return d.selectorStr
          .toLowerCase()
          .match(".*" + this.state.selectorText.toLowerCase() + ".*");
      });
    }
    if (this.state.fileText != "All Files") {
      data = data.filter(d => {
        return d.filePath.match(this.state.fileText);
      });
    }
    if (this.state.projectText != "All Projects") {
      data = data.filter(d => {
        return d.projectName.match(this.state.projectText);
      });
    }

    const columns = [
      {
        Header: "Selector ID",
        accessor: "index",
        id: "index",
        show: false
      },
      {
        Header: "Selector",
        accessor: "selectorStr"
      },
      {
        Header: "File",
        accessor: "filePath"
      },
      {
        Header: "Project",
        accessor: "projectName"
      }
    ];
    return (
      <React.Fragment>
        <div className="row justify-content-lg-left">
          <div className="col-lg-12">
            <div className="ml-4 mt-4 mb-4">
              <span className="heading-1 d-block">Selectors Overview</span>
              <span className="heading-2 mb-3 d-block">
                Here is a table of all selectors.
              </span>
            </div>
            <div className="ml-4 mt-4 mb-4" id="stFilters">
              <div
                className="form-group has-search d-inline-block"
                style={{ width: "185px" }}
              >
                <span className="fa fa-search form-control-feedback"></span>
                <input
                  type="text"
                  className="form-control input-custom"
                  placeholder="Name Search"
                  id="stNameFilter"
                  onChange={() =>
                    this.setState({ selectorText: event.target.value })
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
                  id="stFileFilter"
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
                      key={"stfile" + f.index}
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
                  id="stProjectFilter"
                >
                  {this.state.projectText}
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {project.map(p => (
                    <li
                      className="dropdown-item"
                      key={"stproject" + p.index}
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
