export default function StocKTable(props) {

    var list = [];
    let i =0;
    // console.log("=====",props.records)
    let data = props.records
    if (data != undefined) {
        data.forEach(element => {
            // let id = element[0]
            // element = element[1]
            console.log(element)
            list.push(
                
                
                // <tr id={i} key={i} className="record_row">
                //     <td><div >{element[0]}</div></td>
                //     <td><div >{element[1]}</div></td>
                //     <td><div >{element[2]}</div></td>
                // </tr>
            )
            i += 1
        });
    }
    
    return list;
}
