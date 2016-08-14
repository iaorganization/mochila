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
import javax.swing.JPanel;

public class GraficoDinamico {

    private static final int TIPO_GRAFICO_TEMPO_FITNESS = 0;
    private static final int TIPO_GRAFICO_PESO_FITNESS = 1;
    
    public static void main(String[] args) {
        
        List<String> dadosPython1Genetico = new ArrayList<>(100000);
        List<String> dadosPython2Genetico = new ArrayList<>(100000);
        List<String> dadosPython3Genetico = new ArrayList<>(100000);
        
        List<String> dadosPython1PSO = new ArrayList<>(100000);
        List<String> dadosPython2PSO = new ArrayList<>(100000);
        List<String> dadosPython3PSO = new ArrayList<>(100000);
        
        List<String> dadosPython1Todos = new ArrayList<>(100000);
        List<String> dadosPython2Todos = new ArrayList<>(100000);
        List<String> dadosPython3Todos = new ArrayList<>(100000);
        
        Chart2D graficoGenetico = new Chart2D();
        Chart2D graficoPSO = new Chart2D();
        Chart2D graficoTodos = new Chart2D();

        ITrace2D trace1Genetico = new Trace2DLtd(500);
        ITrace2D trace2Genetico = new Trace2DLtd(500);
        ITrace2D trace3Genetico = new Trace2DLtd(500);
        
        ITrace2D trace1PSO = new Trace2DLtd(500);
        ITrace2D trace2PSO = new Trace2DLtd(500);
        ITrace2D trace3PSO = new Trace2DLtd(500);
        
        ITrace2D trace1Todos = new Trace2DLtd(500);
        ITrace2D trace2Todos = new Trace2DLtd(500);
        ITrace2D trace3Todos = new Trace2DLtd(500);

        trace1Genetico.setColor(Color.RED);
        trace1Genetico.setName("Execucao 1");
        trace2Genetico.setColor(Color.BLUE);
        trace2Genetico.setName("Execucao 2");
        trace3Genetico.setColor(Color.BLACK);
        trace3Genetico.setName("Execucao 3");
        
        trace1PSO.setColor(Color.RED);
        trace1PSO.setName("Execucao 1");
        trace2PSO.setColor(Color.BLUE);
        trace2PSO.setName("Execucao 2");
        trace3PSO.setColor(Color.BLACK);
        trace3PSO.setName("Execucao 3");
        
        trace1Todos.setColor(Color.RED);
        trace1Todos.setName("Genetico");
        trace2Todos.setColor(Color.BLUE);
        trace2Todos.setName("PSO");
        trace3Todos.setColor(Color.BLACK);
        trace3Todos.setName("Aleatorio");
        
        trace1Todos.setTracePainter(new TracePainterDisc(4));
        trace2Todos.setTracePainter(new TracePainterDisc(4));
        trace3Todos.setTracePainter(new TracePainterDisc(4));
        
        configuraLimiteEixos(graficoTodos, 25000, 45000);
        
        graficoGenetico.addTrace(trace1Genetico);
        graficoGenetico.addTrace(trace2Genetico);
        graficoGenetico.addTrace(trace3Genetico);
        graficoGenetico.getAxisX().setAxisTitle(new IAxis.AxisTitle("Geracao"));
        graficoGenetico.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));
        
        graficoPSO.addTrace(trace1PSO);
        graficoPSO.addTrace(trace2PSO);
        graficoPSO.addTrace(trace3PSO);
        graficoPSO.getAxisX().setAxisTitle(new IAxis.AxisTitle("Epoca"));
        graficoPSO.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));
        
        graficoTodos.addTrace(trace1Todos);
        graficoTodos.addTrace(trace2Todos);
        graficoTodos.addTrace(trace3Todos);
        graficoTodos.getAxisX().setAxisTitle(new IAxis.AxisTitle("Peso"));
        graficoTodos.getAxisY().setAxisTitle(new IAxis.AxisTitle("Fitness"));

        Timer timerGenetico = new Timer(true);
        TimerTask taskGenetico = criaTarefa(dadosPython1Genetico, trace1Genetico, dadosPython2Genetico, trace2Genetico, dadosPython3Genetico, trace3Genetico, TIPO_GRAFICO_TEMPO_FITNESS);

        JButton btnStartGenetico = new javax.swing.JButton("Start Genetico");
        JButton btnCapturaDadosGenetico = new javax.swing.JButton("Captura Dados");
        btnCapturaDadosGenetico.setEnabled(false);
        JButton btnStopGenetico = new javax.swing.JButton("Stop");
        btnStopGenetico.setEnabled(false);

        btnStartGenetico.addActionListener(e -> {
            Runnable task2 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython1Genetico);
            };
            new Thread(task2).start();

            Runnable task3 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython2Genetico);
            };
            new Thread(task3).start();

            Runnable task4 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython3Genetico);
            };
            new Thread(task4).start();
            btnStartGenetico.setEnabled(false);
            btnCapturaDadosGenetico.setEnabled(true);
        });

        btnCapturaDadosGenetico.addActionListener(e -> {
            startCapturaDados(timerGenetico, taskGenetico);
            btnCapturaDadosGenetico.setEnabled(false);
            btnStopGenetico.setEnabled(true);
                });
        
        btnStopGenetico.addActionListener(e -> {
            stopCapturaDados(timerGenetico, taskGenetico);
            btnStopGenetico.setEnabled(false);
                });

        Timer timerPSO = new Timer(true);
        TimerTask taskPSO = criaTarefa(dadosPython1PSO, trace1PSO, dadosPython2PSO, trace2PSO, dadosPython3PSO, trace3PSO, TIPO_GRAFICO_TEMPO_FITNESS);

        JButton btnStartPSO = new javax.swing.JButton("Start PSO");
        JButton btnCapturaDadosPSO = new javax.swing.JButton("Captura Dados");
        btnCapturaDadosPSO.setEnabled(false);
        JButton btnStopPSO = new javax.swing.JButton("Stop");
        btnStopPSO.setEnabled(false);

        btnStartPSO.addActionListener(e -> {
            Runnable task2 = () -> {
                executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dadosPython1PSO);
            };
            new Thread(task2).start();

            Runnable task3 = () -> {
                executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dadosPython2PSO);
            };
            new Thread(task3).start();

            Runnable task4 = () -> {
                executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dadosPython3PSO);
            };
            new Thread(task4).start();
            btnStartPSO.setEnabled(false);
            btnCapturaDadosPSO.setEnabled(true);
        });

        btnCapturaDadosPSO.addActionListener(e -> {
            startCapturaDados(timerPSO, taskPSO);
            btnCapturaDadosPSO.setEnabled(false);
            btnStopPSO.setEnabled(true);
                });
        btnStopPSO.addActionListener(e -> {
            stopCapturaDados(timerPSO, taskPSO);
            btnStopPSO.setEnabled(false);
                });

        Timer timerTodos = new Timer(true);
        TimerTask taskTodos = criaTarefa(dadosPython1Todos, trace1Todos, dadosPython2Todos, trace2Todos, dadosPython3Todos, trace3Todos, TIPO_GRAFICO_PESO_FITNESS);
        
        JButton btnStartTodos = new javax.swing.JButton("Start Todos");
        JButton btnCapturaDadosTodos = new javax.swing.JButton("Captura Dados");
        btnCapturaDadosTodos.setEnabled(false);
        JButton btnStopTodos = new javax.swing.JButton("Stop");
        btnStopTodos.setEnabled(false);

        btnStartTodos.addActionListener(e -> {
            Runnable task2 = () -> {
                executaPrograma("python main_genetico.py", "exit.txt", "erro.txt", dadosPython1Todos);
            };
            new Thread(task2).start();

            Runnable task3 = () -> {
                executaPrograma("python main_pso.py", "exit.txt", "erro.txt", dadosPython2Todos);
            };
            new Thread(task3).start();

            Runnable task4 = () -> {
                executaPrograma("python main_aleatorio.py", "exit.txt", "erro.txt", dadosPython3Todos);
            };
            new Thread(task4).start();
            btnStartTodos.setEnabled(false);
            btnCapturaDadosTodos.setEnabled(true);
        });

        btnCapturaDadosTodos.addActionListener(e -> {
            startCapturaDados(timerTodos, taskTodos);
            btnCapturaDadosTodos.setEnabled(false);
            btnStopTodos.setEnabled(true);
                });
        btnStopTodos.addActionListener(e -> {
            stopCapturaDados(timerTodos, taskTodos);
            btnStopTodos.setEnabled(false);
                });
        
        JFrame frame = new JFrame("Inteligencia Artificial");

        Container c = frame.getContentPane();
        JPanel jp = new JPanel(new GridLayout(1,3,50,50));

        JPanel jpGenetico = new JPanel(new BorderLayout());
        JPanel jpGeneticoTopo = new JPanel();
        jpGeneticoTopo.add(btnStartGenetico);
        jpGeneticoTopo.add(btnCapturaDadosGenetico);
        jpGeneticoTopo.add(btnStopGenetico);        
        jpGenetico.add(jpGeneticoTopo, BorderLayout.NORTH);
        jpGenetico.add(graficoGenetico, BorderLayout.CENTER);

        JPanel jpPSO = new JPanel(new BorderLayout());
        JPanel jpPSOTopo = new JPanel();
        jpPSOTopo.add(btnStartPSO);
        jpPSOTopo.add(btnCapturaDadosPSO);
        jpPSOTopo.add(btnStopPSO);        
        jpPSO.add(jpPSOTopo, BorderLayout.NORTH);
        jpPSO.add(graficoPSO, BorderLayout.CENTER); 
        
        JPanel jpTodos = new JPanel(new BorderLayout());
        JPanel jpTodosTopo = new JPanel();
        jpTodosTopo.add(btnStartTodos);
        jpTodosTopo.add(btnCapturaDadosTodos);
        jpTodosTopo.add(btnStopTodos);        
        jpTodos.add(jpTodosTopo, BorderLayout.NORTH);
        jpTodos.add(graficoTodos, BorderLayout.CENTER);
        
        jp.add(jpGenetico);
        jp.add(jpPSO);
        jp.add(jpTodos);
        
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

    private static void centralizaJanela(JFrame frame) throws HeadlessException {
        Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
        frame.setLocation(dim.width / 2 - frame.getSize().width / 2,
                dim.height / 2 - frame.getSize().height / 2);
    }

    private static TimerTask criaTarefa(List<String> dadosPython, ITrace2D trace, List<String> dadosPython2, ITrace2D trace2, List<String> dadosPython3, ITrace2D trace3, int tipoGrafico) {
        TimerTask task = new TimerTask() {

            @Override
            public void run() {

                if (!dadosPython.isEmpty() && dadosPython.get(0).contains("-")) {
                    String dados[] = dadosPython.get(0).split("-");
                    dadosPython.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    if (tipoGrafico == TIPO_GRAFICO_TEMPO_FITNESS)
                        trace.addPoint(geracao, valor);
                    else if (tipoGrafico == TIPO_GRAFICO_PESO_FITNESS)
                        trace.addPoint(peso, valor);
                }

                if (!dadosPython2.isEmpty() && dadosPython2.get(0).contains("-")) {
                    String dados[] = dadosPython2.get(0).split("-");
                    dadosPython2.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    if (tipoGrafico == TIPO_GRAFICO_TEMPO_FITNESS)
                        trace2.addPoint(geracao, valor);
                    else if (tipoGrafico == TIPO_GRAFICO_PESO_FITNESS)
                        trace2.addPoint(peso, valor);
                }

                if (!dadosPython3.isEmpty() && dadosPython3.get(0).contains("-")) {
                    String dados[] = dadosPython3.get(0).split("-");
                    dadosPython3.remove(0);
                    int geracao = Integer.parseInt(dados[1]);
                    int peso = Integer.parseInt(dados[3]);
                    int valor = Integer.parseInt(dados[5]);
                    if (tipoGrafico == TIPO_GRAFICO_TEMPO_FITNESS)
                        trace3.addPoint(geracao, valor);
                    else if (tipoGrafico == TIPO_GRAFICO_PESO_FITNESS)
                        trace3.addPoint(peso, valor);
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
        task.cancel();
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
