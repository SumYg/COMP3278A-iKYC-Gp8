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
                    <td><div >{element}</div></td>
                </tr>
            )
            i += 1
        });
    }
    return list;
}
