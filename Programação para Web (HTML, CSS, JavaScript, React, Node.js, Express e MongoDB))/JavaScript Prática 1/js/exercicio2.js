function tratadorDeCliqueExercicio2() {
    // atualize esta função para
    // exibir um alerta com a hora 
    // atual no seguinte formato:
    // Horário: 8 PM : 40m : 28s
    let horario = new Date()
    let hora = horario.getHours()
    if (hora >= 12) {
        var pm_am = 'PM'
        var hora_pm_am = hora % 12
    } else {
        var pm_am = 'AM'
        if (hora == 0){
            var hora_pm_am = 12
        }
    }
    let minuto = horario.getMinutes()
    let segundo = horario.getSeconds()
    console.log(`Horário: ${hora_pm_am} ${pm_am} : ${minuto}m : ${segundo}s`)
}