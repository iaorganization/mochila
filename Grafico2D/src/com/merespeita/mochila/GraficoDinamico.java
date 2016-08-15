package com.merespeita.mochila;

import info.monitorenter.gui.chart.Chart2D;
import info.monitorenter.gui.chart.IAxis;
import info.monitorenter.gui.chart.IAxisScalePolicy;
import info.monitorenter.gui.chart.IRangePolicy;
import info.monitorenter.gui.chart.ITrace2D;
import info.monitorenter.gui.chart.axis.scalepolicy.AxisScalePolicyManualTicks;
import info.monitorenter.gui.chart.rangepolicies.RangePolicyFixedViewport;
import info.monitorenter.gui.chart.traces.Trace2DLtd;
import info.monitorenter.gui.chart.traces.painters.TracePainterDisc;
import info.monitorenter.util.Range;
import java.awt.BorderLayout;

import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.GridLayout;
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
import javax.swing.JLabel;
import javax.swing.JPanel;

public class GraficoDinamico {

    private static final int TIPO_GRAFICO_TEMPO_FITNESS = 0;
    private static final int TIPO_GRAFICO_PESO_FITNESS = 1;
    
    private static JLabel labelGenetico, labelPSO, labelAleatorio;
    private static List<List<String>> dadosGenetico, dadosPSO, dadosAleatorio;
    private static Chart2D graficoGenetico, graficoPSO, graficoAleatorio;
    private static List<ITrace2D> tracesGenetico, tracesPSO, tracesAleatorio;
    private static Timer timerGenetico, timerPSO, timerAleatorio;
    private static TimerTask taskGenetico, taskPSO, taskAleatorio;
    private static JButton btnGeneticoStart, btnGeneticoCaptura, btnGeneticoStop, btnPSOStart, btnPSOCaptura, btnPSOStop, btnAleatorioStart, btnAleatorioCaptura, btnAleatorioStop;
    
    public static void main(String[] args) {
        inicializaGraficos();
        inicializaTimers();
        criaInterface();
        configuraLayout();
    }

    private static void centralizaJanela(JFrame frame) throws HeadlessException {
        Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
        frame.setLocation(dim.width / 2 - frame.getSize().width / 2,
                dim.height / 2 - frame.getSize().height / 2);
    }
    
    private static void configuraLayout(){
        JFrame frame = new JFrame("Inteligencia Artificial");

        Container c = frame.getContentPane();
        JPanel jp = new JPanel(new GridLayout(1,3,50,50));

        JPanel jpGenetico = new JPanel(new BorderLayout());
        JPanel jpGeneticoTopo = new JPanel();
        jpGeneticoTopo.add(btnGeneticoStart);
        jpGeneticoTopo.add(btnGeneticoCaptura);
        jpGeneticoTopo.add(btnGeneticoStop);        
        jpGenetico.add(jpGeneticoTopo, BorderLayout.NORTH);
        jpGenetico.add(graficoGenetico, BorderLayout.CENTER);
        jpGenetico.add(labelGenetico, BorderLayout.SOUTH);

        JPanel jpPSO = new JPanel(new BorderLayout());
        JPanel jpPSOTopo = new JPanel();
        jpPSOTopo.add(btnPSOStart);
        jpPSOTopo.add(btnPSOCaptura);
        jpPSOTopo.add(btnPSOStop);        
        jpPSO.add(jpPSOTopo, BorderLayout.NORTH);
        jpPSO.add(graficoPSO, BorderLayout.CENTER);
        jpPSO.add(labelPSO, BorderLayout.SOUTH);
        
        JPanel jpAleatorio = new JPanel(new BorderLayout());
        JPanel jpAleatorioTopo = new JPanel();
        jpAleatorioTopo.add(btnAleatorioStart);
        jpAleatorioTopo.add(btnAleatorioCaptura);
        jpAleatorioTopo.add(btnAleatorioStop);
        jpAleatorio.add(jpAleatorioTopo, BorderLayout.NORTH);
        jpAleatorio.add(graficoAleatorio, BorderLayout.CENTER);
        jpAleatorio.add(labelAleatorio, BorderLayout.SOUTH);
        
        jp.add(jpGenetico);
        jp.add(jpPSO);
        jp.add(jpAleatorio);
        
        c.add(jp);
        frame.setSize(1300, 400);

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

    private static void criaInterface(){
        btnGeneticoStart = new javax.swing.JButton("Start Genetico");
        btnGeneticoCaptura = new javax.swing.JButton("Captura Dados");
        btnGeneticoCaptura.setEnabled(false);
        btnGeneticoStop = new javax.swing.JButton("Stop");
        btnGeneticoStop.setEnabled(false);
        btnGeneticoStart.addActionListener(e -> {
            for (int i = 0; i < dadosGenetico.size(); i++) {
                List<String> dGenetico = dadosGenetico.get(i);
                Runnable task = () -> {
                    executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dGenetico);
                };
                new Thread(task).start();
            }
            btnGeneticoStart.setEnabled(false);
            btnGeneticoCaptura.setEnabled(true);
        });
        btnGeneticoCaptura.addActionListener(e -> {
            startCapturaDados(timerGenetico, taskGenetico);
            btnGeneticoCaptura.setEnabled(false);
            btnGeneticoStop.setEnabled(true);
                });
        btnGeneticoStop.addActionListener(e -> {
            stopCapturaDados(timerGenetico, taskGenetico);
            btnGeneticoStop.setEnabled(false);
                });
        
        btnPSOStart = new javax.swing.JButton("Start PSO");
        btnPSOCaptura = new javax.swing.JButton("Captura Dados");
        btnPSOCaptura.setEnabled(false);
        btnPSOStop = new javax.swing.JButton("Stop");
        btnPSOStop.setEnabled(false);
        btnPSOStart.addActionListener(e -> {
            for (int i = 0; i < dadosPSO.size(); i++) {
                List<String> dPSO = dadosPSO.get(i);
                Runnable task = () -> {
                    executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dPSO);
                };
                new Thread(task).start();
                
            }
            btnPSOStart.setEnabled(false);
            btnPSOCaptura.setEnabled(true);
        });
        btnPSOCaptura.addActionListener(e -> {
            startCapturaDados(timerPSO, taskPSO);
            btnPSOCaptura.setEnabled(false);
            btnPSOStop.setEnabled(true);
                });
        btnPSOStop.addActionListener(e -> {
            stopCapturaDados(timerPSO, taskPSO);
            btnPSOStop.setEnabled(false);
                });
        
        btnAleatorioStart = new javax.swing.JButton("Start Aleatorio");
        btnAleatorioCaptura = new javax.swing.JButton("Captura Dados");
        btnAleatorioCaptura.setEnabled(false);
        btnAleatorioStop = new javax.swing.JButton("Stop");
        btnAleatorioStop.setEnabled(false);

        btnAleatorioStart.addActionListener(e -> {
            Runnable task2 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosAleatorio.get(0));
            };
            new Thread(task2).start();

            Runnable task3 = () -> {
                executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dadosAleatorio.get(1));
            };
            new Thread(task3).start();

            Runnable task4 = () -> {
                executaPrograma("python main_aleatorio.py", "exit.txt", "erro.txt", dadosAleatorio.get(2));
            };
            new Thread(task4).start();
            btnAleatorioStart.setEnabled(false);
            btnAleatorioCaptura.setEnabled(true);
        });
        btnAleatorioCaptura.addActionListener(e -> {
            startCapturaDados(timerAleatorio, taskAleatorio);
            btnAleatorioCaptura.setEnabled(false);
            btnAleatorioStop.setEnabled(true);
                });
        btnAleatorioStop.addActionListener(e -> {
            stopCapturaDados(timerAleatorio, taskAleatorio);
            btnAleatorioStop.setEnabled(false);
                });
    }
    
    private static TimerTask criaTarefa(List<List<String>> dadosPython, List<ITrace2D> traces, int tipoGrafico) {
        TimerTask task = new TimerTask() {
            @Override
            public void run() {
                for (int i = 0; i < dadosPython.size(); i++) {
                    List<String> dPython = dadosPython.get(i);
                    ITrace2D trace = traces.get(i);
                    
                    if (!dPython.isEmpty() && dPython.get(0).contains("-")) {
                        String dados[] = dPython.get(0).split("-");
                        dPython.remove(0);
                        int geracao = Integer.parseInt(dados[1]);
                        int peso = Integer.parseInt(dados[3]);
                        int valor = Integer.parseInt(dados[5]);
                        if (tipoGrafico == TIPO_GRAFICO_TEMPO_FITNESS)
                            trace.addPoint(geracao, valor);
                        else if (tipoGrafico == TIPO_GRAFICO_PESO_FITNESS)
                            trace.addPoint(peso, valor);
                    }
                }
            }
        };
        return task;
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
    
    private static void inicializaGraficos(){
        dadosGenetico = new ArrayList<>(3);
        dadosPSO = new ArrayList<>(3);
        dadosAleatorio = new ArrayList<>(3);
        
        tracesGenetico = new ArrayList<>(3);
        tracesPSO = new ArrayList<>(3);
        tracesAleatorio = new ArrayList<>(3);
        
        for (int i = 0; i < 3; i ++){
            dadosGenetico.add(new ArrayList<>(100000));    
            dadosPSO.add(new ArrayList<>(1000000));
            dadosAleatorio.add(new ArrayList<>(1000000));
            
            tracesGenetico.add(new Trace2DLtd(500));
            tracesPSO.add(new Trace2DLtd(500));
            tracesAleatorio.add(new Trace2DLtd(500));
        }
        
        graficoGenetico = new Chart2D();
        graficoPSO = new Chart2D();
        graficoAleatorio = new Chart2D();
        
        labelGenetico = new JLabel("Saida: ");
        labelPSO = new JLabel("Saida: ");
        labelAleatorio = new JLabel("Saida: ");

        tracesGenetico.get(0).setColor(Color.RED);
        tracesGenetico.get(0).setName("Execucao 1");
        tracesGenetico.get(1).setColor(Color.BLUE);
        tracesGenetico.get(1).setName("Execucao 2");
        tracesGenetico.get(2).setColor(Color.BLACK);
        tracesGenetico.get(2).setName("Execucao 3");
        
        tracesPSO.get(0).setColor(Color.RED);
        tracesPSO.get(0).setName("Execucao 1");
        tracesPSO.get(1).setColor(Color.BLUE);
        tracesPSO.get(1).setName("Execucao 2");
        tracesPSO.get(2).setColor(Color.BLACK);
        tracesPSO.get(2).setName("Execucao 3");
        
        tracesAleatorio.get(0).setColor(Color.RED);
        tracesAleatorio.get(0).setName("Genetico");
        tracesAleatorio.get(1).setColor(Color.BLUE);
        tracesAleatorio.get(1).setName("PSO");
        tracesAleatorio.get(2).setColor(Color.BLACK);
        tracesAleatorio.get(2).setName("Aleatorio");
        
        for (int i = 0; i < tracesAleatorio.size(); i++) {
            tracesAleatorio.get(i).setTracePainter(new TracePainterDisc(3));
        }
        
        for (int i = 0; i < 3; i++) {
            graficoGenetico.addTrace(tracesGenetico.get(i));
            graficoPSO.addTrace(tracesPSO.get(i));
            graficoAleatorio.addTrace(tracesAleatorio.get(i));
        }
        
        configuraLimiteEixos(graficoAleatorio, 25000, 45000);
        
        graficoGenetico.getAxisX().setAxisTitle(new IAxis.AxisTitle("Geracao"));
        graficoGenetico.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));
        
        graficoPSO.getAxisX().setAxisTitle(new IAxis.AxisTitle("Epoca"));
        graficoPSO.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));
        
        graficoAleatorio.getAxisX().setAxisTitle(new IAxis.AxisTitle("Peso"));
        graficoAleatorio.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));
    }
    
    private static void inicializaTimers(){
        timerGenetico = new Timer(true);
        taskGenetico = criaTarefa(dadosGenetico, tracesGenetico, TIPO_GRAFICO_TEMPO_FITNESS);
        timerPSO = new Timer(true);
        taskPSO = criaTarefa(dadosPSO, tracesPSO, TIPO_GRAFICO_TEMPO_FITNESS);        
        timerAleatorio = new Timer(true);
        taskAleatorio = criaTarefa(dadosAleatorio, tracesAleatorio, TIPO_GRAFICO_PESO_FITNESS);
    }
    
    private static void startCapturaDados(Timer timer, TimerTask task) {
        timer.schedule(task, 300, 300);
    }

    private static void stopCapturaDados(Timer timer, TimerTask task) {
        timer.cancel();
        task.cancel();
    }
}
