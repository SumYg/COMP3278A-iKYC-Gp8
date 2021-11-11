import React, { useState, useEffect } from 'react';
export default function RealTimeStockTable(props) {
    const [data, setData] = useState(props.records);
    const update = () => {
        fetch('http://localhost:8080/getStock').then(response => {
            if (response.status === 200) {
              response.json().then( res => {
                console.log("Get")
                console.log(res)
                setData(res['data'])
            })
            } else {
              alert("Server return status "+response.status)
            }
          })
    }

    useEffect(
        () => {
            console.log("UserEffect()")
            const id = setInterval(update, 30000);
            return () => clearInterval(id);
        }
    );

    return <StocKTable records={data}/>;
}


function StocKTable(props) {
    var list = [];
    let i =0;
    console.log("=====",props.records)
    let data = props.records
    if (data !== undefined) {
        data.forEach(element => {
            // let id = element[0]
            // element = element[1]
            console.log("StockTable update")
            list.push(
                
                <tr id={i} key={i} className="record_row">
                    <td><div >{element[0]}</div></td>
                    <td><div >{element[1]}</div></td>
                    <td><div >{element[2]}</div></td>
                </tr>
            )
            i += 1
        });
    }
    
    return list;
}
