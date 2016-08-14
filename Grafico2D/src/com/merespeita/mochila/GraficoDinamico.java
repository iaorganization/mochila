package com.merespeita.mochila;

import info.monitorenter.gui.chart.Chart2D;
import info.monitorenter.gui.chart.IAxis;
import info.monitorenter.gui.chart.IAxisScalePolicy;
import info.monitorenter.gui.chart.IRangePolicy;
import info.monitorenter.gui.chart.ITrace2D;
import info.monitorenter.gui.chart.axis.scalepolicy.AxisScalePolicyManualTicks;
import info.monitorenter.gui.chart.rangepolicies.RangePolicyFixedViewport;
import info.monitorenter.gui.chart.traces.Trace2DLtd;
import info.monitorenter.util.Range;
import java.awt.BorderLayout;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.HeadlessException;
import java.awt.Toolkit;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import javax.swing.JButton;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class GraficoDinamico {

    public static void main(String[] args) {
        
        List<String> dadosPython = new ArrayList<>(100000);
        List<String> dadosPython2 = new ArrayList<>(100000);
        List<String> dadosPython3 = new ArrayList<>(100000);

        Chart2D chart = new Chart2D();
        Chart2D chart2 = new Chart2D();

        ITrace2D trace = new Trace2DLtd(500);
        trace.setColor(Color.RED);

        ITrace2D trace2 = new Trace2DLtd(500);
        trace2.setColor(Color.BLUE);

        ITrace2D trace3 = new Trace2DLtd(500);
        trace3.setColor(Color.BLACK);

//        configuraLimiteEixos(chart, 25000, 45000);
        
        chart.addTrace(trace);
        chart.addTrace(trace2);
        chart.addTrace(trace3);
//        trace.setTracePainter(new TracePainterDisc(4));
//        trace2.setTracePainter(new TracePainterDisc(4));
//        trace3.setTracePainter(new TracePainterDisc(4));

        Timer timer = new Timer(true);
        TimerTask task = criaTarefa(dadosPython, trace, dadosPython2, trace2, dadosPython3, trace3);

        JButton btnStartGenetico = new javax.swing.JButton("Start Genetico");
        JButton btnCapturaDados = new javax.swing.JButton("Captura Dados");
        btnCapturaDados.setEnabled(false);
        JButton btnStop = new javax.swing.JButton("Stop");
        btnStop.setEnabled(false);

        btnStartGenetico.addActionListener(e -> {
            Runnable task2 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython);
            };
            new Thread(task2).start();

            Runnable task3 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython2);
            };
            new Thread(task3).start();

            Runnable task4 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython3);
            };
            new Thread(task4).start();
            btnStartGenetico.setEnabled(false);
            btnCapturaDados.setEnabled(true);
            btnStop.setEnabled(true);
        });

        btnCapturaDados.addActionListener(e -> startCapturaDados(timer, task));

        btnStop.addActionListener(e -> stopCapturaDados(timer, task));

        JFrame frame = new JFrame("Algoritmo Genetico");

        Container c = frame.getContentPane();

        JPanel jp = new JPanel();

        jp.add(btnStartGenetico);
        jp.add(btnCapturaDados);
        jp.add(btnStop);

        c.add(jp, BorderLayout.NORTH);

        c.add(chart, BorderLayout.CENTER);

        frame.setSize(600, 600);

        centralizaJanela(frame);

        frame.addWindowListener(
                new WindowAdapter() {
                    @Override
                    public void windowClosing(WindowEvent e) {
                        System.exit(0);
                    }
                }
        );

        frame.setVisible(true);

    }

    private static void configuraLimiteEixos(Chart2D chart, int min, int max) {
        IAxis<IAxisScalePolicy> xAxis = (IAxis<IAxisScalePolicy>) chart.getAxisX();
        xAxis.setAxisScalePolicy(new AxisScalePolicyManualTicks());
        xAxis.setMajorTickSpacing(max);
        xAxis.setMinorTickSpacing(min);
        xAxis.setStartMajorTick(true);

        IAxis<IAxisScalePolicy> yAxis = (IAxis<IAxisScalePolicy>) chart.getAxisY();
        yAxis.setAxisScalePolicy(new AxisScalePolicyManualTicks());
        yAxis.setMajorTickSpacing(max);
        yAxis.setMinorTickSpacing(min);
        yAxis.setStartMajorTick(true);

        IRangePolicy rangePolicyX = new RangePolicyFixedViewport(new Range(min, max));
        xAxis.setRangePolicy(rangePolicyX);

        IRangePolicy rangePolicyY = new RangePolicyFixedViewport(new Range(min, max));
        yAxis.setRangePolicy(rangePolicyY);
    }

    private static void centralizaJanela(JFrame frame) throws HeadlessException {
        Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
        frame.setLocation(dim.width / 2 - frame.getSize().width / 2,
                dim.height / 2 - frame.getSize().height / 2);
    }

    private static TimerTask criaTarefa(List<String> dadosPython, ITrace2D trace, List<String> dadosPython2, ITrace2D trace2, List<String> dadosPython3, ITrace2D trace3) {
        TimerTask task = new TimerTask() {

            @Override
            public void run() {

                if (!dadosPython.isEmpty() && dadosPython.get(0).contains("-")) {
                    String dados[] = dadosPython.get(0).split("-");
                    dadosPython.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    trace.addPoint(geracao, valor);
                    System.out.println(valor + "," + peso);
                }

                if (!dadosPython2.isEmpty() && dadosPython2.get(0).contains("-")) {
                    String dados[] = dadosPython2.get(0).split("-");
                    dadosPython2.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    trace2.addPoint(geracao, valor);;   
                }

                if (!dadosPython3.isEmpty() && dadosPython3.get(0).contains("-")) {
                    String dados[] = dadosPython3.get(0).split("-");
                    dadosPython3.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    trace3.addPoint(geracao, valor);
                }

            }

        };
        return task;
    }

    private static void startCapturaDados(Timer timer, TimerTask task) {
        timer.schedule(task, 1000, 20);
    }

    private static void stopCapturaDados(Timer timer, TimerTask task) {
        timer.cancel();
    }

    public static void executaPrograma(String comando, String arquivoSaida, String arquivoErro, List<String> dadosPython) {

        try {
            FileOutputStream fosError = new FileOutputStream(arquivoErro);
            FileOutputStream fosExit = new FileOutputStream(arquivoSaida);

            Runtime rt = Runtime.getRuntime();
            Process proc = rt.exec(comando);

            StreamGobbler errorGobbler = new StreamGobbler(proc.getErrorStream(), "E", fosError);

            StreamGobbler outputGobbler = new StreamGobbler(proc.getInputStream(), "O", fosExit);
            outputGobbler.dados = dadosPython;

            errorGobbler.start();
            outputGobbler.start();

            int exitVal = proc.waitFor();
        } catch (IOException | InterruptedException t) {
            t.printStackTrace();
        }
    }

}
