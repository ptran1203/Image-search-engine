import React, {Fragment} from 'react';

import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";


export default function News(props)  {

    let {news} = props;
    return(
        <Fragment>
            <div>
                <h4 style={{marginBottom: '3px', padding: '4px 8px 2px'}}>Tin tức</h4>
                <div>
                    {news.map((i, index)=>{

                        return(
                            <New data={i} key={`new-ewash-${index}`}/>
                        )
                    })}
                </div>
            </div>        
        </Fragment>
    )
}
 
const New = props => {

    let {title, thumbnailUrl, content} = props.data;
    return(
        <Fragment>
            <Card style={{margin: '10px auto 15px'}}>
                <CardBody>
                    <div>
                        <img style={{width: '100%'}} src= {thumbnailUrl}/>
                    </div>
                    <div>
                        <p style={{fontSize: '1rem', fontWeight: '500', fontColor: '#332'}}>{title}</p>
                    </div>
                </CardBody>
            </Card>
        </Fragment>
    )
}