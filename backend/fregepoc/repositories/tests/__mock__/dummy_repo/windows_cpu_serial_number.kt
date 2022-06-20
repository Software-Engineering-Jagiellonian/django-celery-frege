package com.includehelp

import java.io.BufferedReader
import java.io.File
import java.io.FileWriter
import java.io.InputStreamReader


/**
 * Method for get Windows Machine CPU Serial Number
 */
fun getWindowsCPUSerialNumber(): String {
    var result = ""
    try {
        val file = File.createTempFile("realhowto", ".vbs")
        file.deleteOnExit()
        val fw = FileWriter(file)
        val vbs1 = """Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colItems = objWMIService.ExecQuery _
   ("Select * from Win32_Processor")
For Each objItem in colItems
    Wscript.Echo objItem.ProcessorId
    exit for  ' do the first cpu only!
Next
"""
        fw.write(vbs1)
        fw.close()
        val p = Runtime.getRuntime().exec("cscript //NoLogo " + file.path)
        val input = BufferedReader(InputStreamReader(p.inputStream))
        var line: String?
        while (input.readLine().also { line = it } != null) {
            result += line
        }
        input.close()
    } catch (E: Exception) {
        System.err.println("Windows CPU Exp : " + E.message)
    }
    return result.trim { it <= ' ' }
}

//Main Function, Program Entry Point
fun main(args: Array<String>) {

    //Call function get CPU Serial Number
    val cpuSerialNumber = getWindowsCPUSerialNumber()

    // Print cpuSerialNumber
    println("Windows Machine CPU Serial Number : $cpuSerialNumber")
}
