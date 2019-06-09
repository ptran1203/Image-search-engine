
import React, {Fragment} from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import TextField from '@material-ui/core/TextField';
import Button from '../components/CustomButtons/Button.jsx'
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import Result from '../reactComponents/Result.jsx';
class SearchPage extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            data: null  ,
            searchUrl: '',
            searched: false,
            imagePreviewUrl: null,
            loading: false
        }
    }
    _submitUrl = () => {
        this.setState({imagePreviewUrl: this.state.searchUrl}, ()=> {
            $.ajax({
                type : 'POST',
                url : "/results",
                dataType: 'json',
                data : {imageUrl: this.state.searchUrl, fromUrl: 1},
                success: resp => {
                    this.setState({data: resp['data']})
                }
            });
        })
    }
    _upload = ()=> {
        $('#upload_input').click();
    }
    _searchUpload = () => {
        var file =$('#upload-file')[0];
        var fd = new FormData(file);
        $.ajax({
            type: 'POST',
            url: '/results',
            data: fd,
            contentType: false,
            cache: false,
            processData: false,
            success: resp => {
                resp = JSON.parse(resp);
                this.setState({data: resp['data']})
            }
        });
    }
    _onChangeFile = (e) =>  {
        e.preventDefault();
        let reader = new FileReader();
        let file = e.target.files[0];
        reader.onloadend = () => {
        this.setState({
            imagePreviewUrl: reader.result
        });
        };
        reader.readAsDataURL(file);
    }
    componentDidMount() {
        Object.defineProperty(Array.prototype, 'chunk_inefficient', {
            value: function(chunkSize) {
                var array=this;
                return [].concat.apply([],
                    array.map(function(elem,i) {
                        return i%chunkSize ? [] : [array.slice(i,i+chunkSize)];
                    })
                );
            }
        });
    }
    render(){
        let {data, searchUrl, loading, imagePreviewUrl} = this.state;
        return(
            <Fragment>
                    <div className="container">
                        <div className={data == null?"search-form":"search-form searched"}>
                            <div className="row" style={{width: '100%'}}>
                                <div className="col-md-8 col-sm-8">
                                    <TextField
                                        placeholder="Đường dẫn"
                                        style={{ margin: 8 }}
                                        fullWidth
                                        margin="normal"
                                        InputLabelProps={{
                                            shrink: true,
                                        }}
                                        onChange={(e)=>{this.setState({searchUrl: e.target.value})}}
                                        value={searchUrl}

                                    />
                                    <Button color="success" onClick={this._submitUrl}>
                                        Tìm
                                    </Button>
                                </div>
                                <div className="col-md-4 col-sm-4">
                                    <form id="upload-file" method="post" enctype="multipart/form-data">
                                        <input onChange={this._onChangeFile} style={{display: "none"}} id="upload_input" name="file" type="file" />
                                        <Button onClick={this._upload} variant="contained" color="info">
                                            Tải ảnh lên&nbsp;
                                            <CloudUploadIcon/>
                                        </Button>
                                        <div>
                                            <Button color="success" onClick={this._searchUpload}>
                                                Tìm
                                            </Button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-4">
                                    {!imagePreviewUrl?null:
                                        <div>
                                            <h4>Tìm kiếm hình ảnh tương tự</h4>
                                            <img style={{width: '100%'}} src={imagePreviewUrl}/>
                                        </div>}
                                </div>
                            </div>
                        </div>
                        {data?
                            <Result data={data}/>
                        :null}
                    </div>
            </Fragment>
        )
    }
}


window.renderPage = (dom, props) => {
    ReactDOM.render(React.createElement((SearchPage), props), dom);
};