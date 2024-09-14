let i=0
let max = 10
async function p() {
    for (let j = 0; j < max; j++) {
        await new Promise(resolve => setTimeout(resolve, 1000))
        console.log(i++)
    }
}     
p()