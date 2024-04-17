function tratadorDeCliqueExercicio2() {
    // atualize esta função para
    // exibir um alerta com a hora 
    // atual no seguinte formato:
    // Horário: 8 PM : 40m : 28s
    horario = new Date()
    hora = horario.getHours()
    if (hora >= 12) {
        pm_am = 'PM'
        hora_pm_am = hora % 12
    } else {
        pm_am = 'AM'
        if (hora == 0){
            hora_pm_am = 12
        }
    }
    minuto = horario.getMinutes()
    segundo = horario.getSeconds()
    console.log(`Horário: ${hora_pm_am} ${pm_am} : ${minuto}m : ${segundo}s`)
}