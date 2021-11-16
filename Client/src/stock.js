import React, { useState, useEffect } from 'react';
export default function RealTimeStockTable(props) {
    const [data, setData] = useState(props.records);
    const update = () => {
        fetch('http://localhost:8080/getStock').then(response => {
            if (response.status === 200) {
              response.json().then( res => {
                console.log("Get")
                // console.log(res)
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
            const id = setInterval(update, 1000);
            return () => clearInterval(id);
        }
    );

    return <StocKTable records={data}/>;
}


function StocKTable(props) {
    var list = [];
    let i =0;
    // console.log("=====",props.records)
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
                    <td><div >{element[3]}</div></td>
                    <td><div >{element[4]}</div></td>
                    <td><div >{element[5]}</div></td>
                    <td><div >{element[6]}</div></td>
                    <td> <Action stockName={element[0]}/></td>
                </tr>
            )
            i += 1
        });
    }
    
    return list;
}

function Action(props) {
    const [state, setState] = useState('show');
    const [inputValue, setInputValue] = useState('');
    let body;
    function updatePosition(condition) {
        console.log(condition, props.stockName, inputValue);
        fetch('http://localhost:8080/updatePosition', {
            method: "POST",
            body: JSON.stringify([props.stockName, inputValue, condition])
          }).then(response => {
            if (response.status === 200) {
              response.json().then( res => {
                if (res) {
                    alert('Updated')
                    setState('show')
                } else {
                    alert('Your investment account dont have enough funds!')
                }
            })
            } else {
              alert("Server return status "+response.status)
            }
          })
    }
    switch(state) {
        case 'show':
            body = <div ><BuyButton setActionState={setState}/> / <SellButton setActionState={setState}/></div>
            break
        case 'buy':
            body = <div><p><input onBlur={e => setInputValue(e.target.value)}></input></p><button onClick={()=>{updatePosition('Buy')}}>Submit</button> / <button onClick={()=>{setState('show')}}>Cancel</button></div>
            break
        default:
            body = <div><p><input onBlur={e => setInputValue(e.target.value)}></input></p><button onClick={()=>{updatePosition('Sell')}}>Submit</button> / <button onClick={()=>{setState('show')}}>Cancel</button></div>

    }
    return body
}

function BuyButton(props) {
    return <button onClick={() => {props.setActionState('buy')}}>Buy</button>
}

function SellButton(props) {
    return <button onClick={() => {props.setActionState('sell')}}>Sell</button>
}
