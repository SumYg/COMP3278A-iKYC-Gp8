export default function ArrayRecords(props) {
    var list = [];
    let i =0;
    // console.log("=====",props.records)
    let data = props.records
    if (data !== undefined) {
        data.forEach(element => {
            // let id = element[0]
            // element = element[1]
            list.push(
                <tr id={i} key={i} className="record_row">
                    <Array2Td records={element}/>
                </tr>
            )
            i += 1
        });
    }
    return list;
}

const Array2Td = (props) => {
    // console.log("=====",props.records)
    let data = props.records
    if (data !== undefined) {
        if (typeof data === 'object') {
            var list
            list = [];
            let i =0;
            data.forEach(element => {
                // let id = element[0]
                // element = element[1]
                list.push(
                    <td><div id={i} key={i}>{element}</div></td>
                )
                i += 1
            });
            return list;
        } else {
            return <td><div >{data}</div></td>
        }
    }
    
    
}
