async function deleteEntry(){
    let response = await fetch("delete/workout_data")
    console.log(await response.json())
}