package com.merespeita.mochila;

import info.monitorenter.gui.chart.ITrace2D;
import java.io.*;
import java.util.List;

class StreamGobbler extends Thread {

    InputStream is;
    String type;
    OutputStream os;
    List<String> dados;

    ITrace2D trace;

    StreamGobbler(InputStream is, String type) {
        this(is, type, null);
    }

    StreamGobbler(InputStream is, String type, OutputStream redirect) {
        this.is = is;
        this.type = type;
        this.os = redirect;
    }

    @Override
    public void run() {
       
        try {
            PrintWriter pw = null;
            if (os != null) {
                pw = new PrintWriter(os);
            }

            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String line = null;
            while ((line = br.readLine()) != null) {
                if (pw != null) {
                    pw.println(line);
                }

                if (line.contains("-")) {
                     dados.add(line);

                }
            }
            if (pw != null) {
                pw.flush();
            }
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }
}
