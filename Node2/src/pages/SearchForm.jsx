
import React, {Fragment} from 'react';
import ReactDOM from 'react-dom';
import withStyles from "@material-ui/core/styles/withStyles";
import ehealth from '../general/i3app'; 
import $ from 'jquery';

class SearchForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            searchUrl: ''
        }
    }
    _submitUrl = () => {
        $.ajax({
            type : 'POST',
            url : "/results",
            dataType: 'json',
            data : {imageUrl: this.state.searchUrl, fromUrl: 1},
            success: (response) => {
                console.log(response);
            }
        });
    }
    _onChangeFile = (e) => {
        var formData = new FormData();
        formData.append('file', e.target.files[0]);
        formData.append('fromUrl', 0);
        $.ajax({
            type : 'POST',
            url : "/results",
            processData: false,
            dataType: false,
            data : {file: e.val(), fromUrl: 0},
            success: (response) => {
                console.log(response);
            }
        });
    }
    render(){
        let {searchUrl} = this.state;
        return(
            <Fragment>
                <div className="container">
                    <div className="row">
                        <div className="col-md-8">
                            <input 
                                onChange={(e)=>{this.setState({searchUrl: e.target.value})}}
                                value={searchUrl}
                            />
                            <button onClick={this._submitUrl}>
                                URL
                            </button>
                        </div>
                        <div className="col-md-4">
                            <input 
                                onChange={this._onChangeFile}
                                type="file"
                            />
                        </div>
                    </div>
                </div>
            </Fragment>
        )
    }
}


window.renderForm = (dom, props) => {
    ReactDOM.render(React.createElement((SearchForm), props), dom);
};