




"Software"), to








"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR









import argparse
import csv
import json
import logging
import math
import os
from collections import Counter, defaultdict, deque, namedtuple
from enum import Enum
from pathlib import Path
from typing import Deque, Dict, Generator, List, NamedTuple, Set, Tuple, Union






Strategy = Enum("Strategy", ["Native", "ReshapedOnlyRHS", "Reshaped"])




class GEMMParam(NamedTuple):
    M: int  
    N: int  
    K: int  
    B: int  
    data_type: str  

    @classmethod
    def parse_from_strs(cls, *M_N_K_B, data_type):
        return cls(*map(int, M_N_K_B), str(data_type))

    def __str__(self):
        return ",".join(map(str, self))



class NativeGEMMConfig(NamedTuple):
    m0: int  
    n0: int  
    k0: int  

    @classmethod
    def parse_from_strs(cls, *args):
        (*mnk,) = map(int, args)
        return cls(*mnk)

    def __str__(self):
        return ",".join(map(str, self))



class ReshapedOnlyRHSGEMMConfig(NamedTuple):
    m0: int  
    n0: int  
    k0: int  
    
    h0: int
    
    interleave_rhs: bool
    
    transpose_rhs: bool
    
    export_to_cl_image_rhs: bool

    @classmethod
    def parse_from_strs(cls, *args):
        (*mnkh, interleave_rhs, transpose_rhs, export_to_cl_image_rhs,) = map(int, args)
        interleave_rhs = interleave_rhs == 1
        transpose_rhs = transpose_rhs == 1
        export_to_cl_image_rhs = export_to_cl_image_rhs == 1
        return cls(*mnkh, interleave_rhs, transpose_rhs, export_to_cl_image_rhs)

    def __str__(self):
        return ",".join(map(str, self))



class ReshapedGEMMConfig(NamedTuple):
    m0: int  
    n0: int  
    k0: int  
    
    v0: int
    
    h0: int
    
    interleave_lhs: bool
    
    interleave_rhs: bool
    
    transpose_rhs: bool
    
    export_to_cl_image_rhs: bool

    @classmethod
    def parse_from_strs(cls, *args):
        (*mnkvh, interleave_lhs, interleave_rhs, transpose_rhs, export_to_cl_image_rhs,) = map(int, args)
        interleave_lhs = interleave_lhs == 1
        interleave_rhs = interleave_rhs == 1
        transpose_rhs = transpose_rhs == 1
        export_to_cl_image_rhs = export_to_cl_image_rhs == 1
        return cls(*mnkvh, interleave_lhs, interleave_rhs, transpose_rhs, export_to_cl_image_rhs)

    def __str__(self):
        return ",".join(map(str, self))



class Measurement(NamedTuple):
    opencl_timer_ms_reshape: float
    opencl_timer_ms_kernel: float

    def get_total_ms(self):
        return self.opencl_timer_ms_reshape + self.opencl_timer_ms_kernel

    def is_close_to(self, other, tol):
        return math.fabs(self.get_total_ms() - other.get_total_ms()) < tol

    def is_better_than(self, other, tol):
        return self.get_total_ms() < other.get_total_ms() and not self.is_close_to(
            other
        )

    def __add__(self, other):
        return Measurement(
            self.opencl_timer_ms_reshape + other.opencl_timer_ms_reshape,
            self.opencl_timer_ms_kernel + other.opencl_timer_ms_kernel,
        )

    def __sub__(self, other):
        return Measurement(
            self.opencl_timer_ms_reshape - other.opencl_timer_ms_reshape,
            self.opencl_timer_ms_kernel - other.opencl_timer_ms_kernel,
        )

    def __mul__(self, other):
        return Measurement(
            self.opencl_timer_ms_reshape * other.opencl_timer_ms_reshape,
            self.opencl_timer_ms_kernel * other.opencl_timer_ms_kernel,
        )

    def __floordiv__(self, other):
        return Measurement(
            self.opencl_timer_ms_reshape // other.opencl_timer_ms_reshape,
            self.opencl_timer_ms_kernel // other.opencl_timer_ms_kernel,
        )

    def __truediv__(self, other):
        return Measurement(
            self.opencl_timer_ms_reshape / other.opencl_timer_ms_reshape,
            self.opencl_timer_ms_kernel / other.opencl_timer_ms_kernel,
        )

    def __pow__(self, power):
        return Measurement(
            self.opencl_timer_ms_reshape ** power, self.opencl_timer_ms_kernel ** power
        )

    def __str__(self):
        return ",".join(map(str, self))



GEMMConfigT = Union[NativeGEMMConfig,
                    ReshapedOnlyRHSGEMMConfig, ReshapedGEMMConfig]



class BenchmarkResult(NamedTuple):
    gemm_param: GEMMParam
    strategy: Strategy
    gemm_config: GEMMConfigT
    measurement: Measurement


class GEMMBenchmarkResultRecorder:
    """ A recorder that records and organises GEMM Benchmark results, and produces various reports on the record.
    """

    SummaryLevel = Enum("SummaryLevel", ["Short", "Detailed"])

    def __init__(self, tol=0.01):
        """ Initializer
        """
        self._benchmark_result_record: List[BenchmarkResult] = []
        
        self._strategies = set()
        self._tol = tol

    def add(self, benchmark_result: BenchmarkResult):
        """ Add a benchmark result to the record.
        """
        gemm_param, strategy, gemm_config, measurement = benchmark_result
        
        self._strategies.add(strategy)

        self._benchmark_result_record.append(benchmark_result)

    def get_record(self) -> Generator[BenchmarkResult, None, None]:
        """ Return an iterator that iterates over the record.
        """
        yield from self._benchmark_result_record

    def get_best_gemm_configs(self):
        """ Get the best GEMMConfig set per GEMMParam per Strategy
        """
        best_gc_sets: Dict[
            Tuple[GEMMParam, Strategy], List[Tuple[GEMMConfig, Measurement]]
        ] = defaultdict(list)
        for gemm_param, strategy, gemm_config, measurement in self.get_record():
            best_gc_set = best_gc_sets.setdefault((gemm_param, strategy), [])
            best_gc_set.append((gemm_config, measurement))
            
            best_gc_set = sorted(
                best_gc_set, key=lambda gc_and_m: gc_and_m[1].get_total_ms()
            )
            
            best_gc, best_m = best_gc_set[0]
            best_gc_set_new = [
                (gemm_config, measurement)
                for gemm_config, measurement in best_gc_set[1:]
                if measurement.is_close_to(best_m, self._tol)
            ]
            
            best_gc_set_new.insert(0, (best_gc, best_m))
            best_gc_sets[(gemm_param, strategy)] = best_gc_set_new

        return best_gc_sets

    def get_best_gemm_configs_as_sequence(self):
        """ Get the best GEMMConfig set per GEMMParam per Strategy, and flatten the result into a sequence
        of BenchmarkResults
        """
        for (
            (gemm_param, strategy),
            best_gc_sets,
        ) in self.get_best_gemm_configs().items():
            for best_gemm_config, best_measurement in best_gc_sets:
                yield BenchmarkResult(
                    gemm_param, strategy, best_gemm_config, best_measurement
                )

    def get_config_distributions(self):
        """ Return GEMMConfigDistribution for each strategy
        """
        gemm_config_distributions: Dict[Strategy, GEMMConfigDistribution] = defaultdict(
            GEMMConfigDistribution
        )
        for benchmark_result in self.get_best_gemm_configs_as_sequence():
            _, strategy, _, _ = benchmark_result
            gemm_config_distributions[strategy].add(benchmark_result)

        return gemm_config_distributions

    def get_best_gemm_strategies(self):
        """ Get the best Stratey per GEMMParam
        """
        all_results: Dict[GEMMParam, List[Tuple[Strategy, Measurement]]] = defaultdict(
            list
        )

        best_strategies: Dict[GEMMParam, Strategy] = {}

        for gemm_param, strategy, gemm_config, measurement in self.get_record():
            all_results[gemm_param].append((strategy, measurement))

        for gemm_param, results_set in all_results.items():
            
            results_set = sorted(
                results_set, key=lambda s_and_m: s_and_m[1].get_total_ms()
            )
            
            best_s, best_m = results_set[0]
            best_strategies[gemm_param] = best_s

        return best_strategies

    def save_to_jsons(self, out_dir, only_best_config=True):
        """ Save records to an output directory of JSON files.
        The directory is organized such that each strategy gets its own JSON file.
        The directory also includes a JSON file to define the best strategy per GEMM Param.
        """
        if not os.path.exists(out_dir):
            logging.info(
                "Output directory {} does not exist. Creating...".format(
                    out_dir)
            )
            os.mkdir(out_dir)

        out_json_path = os.path.join(out_dir, "gemm_type_selection.json")
        if check_out_path(out_json_path):
            results = self.get_best_gemm_strategies()
            results = {str(key): value.name for key, value in results.items()}
            dump_json(out_json_path, results)

        for strategy in self._strategies:
            out_json_path = os.path.join(
                out_dir, ("gemm_config_" + strategy.name.lower() + ".json")
            )
            if check_out_path(out_json_path):
                record = (
                    self.get_best_gemm_configs_as_sequence()
                    if only_best_config
                    else self.get_record()
                )
                results = defaultdict(list)
                for res in record:
                    if res.strategy == strategy:
                        results[str(res.gemm_param)].append(
                            {
                                "GEMMConfig": str(res.gemm_config),
                                "OpenCL_Timer_ms_reshape": str(
                                    res.measurement.opencl_timer_ms_reshape
                                ),
                                "OpenCL_Timer_ms_kernel": str(
                                    res.measurement.opencl_timer_ms_kernel
                                ),
                            }
                        )
                dump_json(out_json_path, results)

    def summary(self, sum_level=SummaryLevel.Short):
        """ Return the summary string of the record
        """
        num_raw_records = sum(1 for _ in self.get_record())
        gemm_params_per_strategy = defaultdict(list)
        for gemm_param, strategy in self.get_best_gemm_configs().keys():
            gemm_params_per_strategy[strategy].append(gemm_param)
        global_summary = f"""
=== {self.__class__.__name__} Summary ===
[Global]
Strategies recorded: {", ".join(map(lambda s: s.name, self._strategies))}
Total number of results recorded: {num_raw_records}

[Per strategy]
        """
        strategy_summaries = []
        for strategy in gemm_params_per_strategy:
            summary = f"""
Strategy {strategy.name}:
GEMM parameters:
    Number of: {len(gemm_params_per_strategy[strategy])}
            """
            if sum_level == self.__class__.SummaryLevel.Detailed:
                summary += f"""
    Content: {gemm_params_per_strategy[strategy]}
                """
            strategy_summaries.append(summary)
        return global_summary + "".join(strategy_summaries)


class GEMMConfigDistribution:
    """ A representation of the GEMM Configuration distribution produced by the GEMMBenchmarkResultRecorder.
    """

    def __init__(self):
        """ Initializer
        """
        self._gemm_config_dist: Dict[
            GEMMConfig, List[Tuple[GEMMParam, Measurement]]
        ] = defaultdict(list)
        self._gemm_config_freq = Counter()

    def add(self, benchmark_result: BenchmarkResult):
        """ Add a benchmark result to the distribution
        """
        gemm_param, _, gemm_config, measurement = benchmark_result
        self._gemm_config_dist[gemm_config].append((gemm_param, measurement))
        self._gemm_config_freq[gemm_config] += 1

    def distribution(self):
        return self._gemm_config_dist

    def frequency(self):
        """ Get the frequency of each (best) gemm config recorded
        """
        return self._gemm_config_freq.most_common()

    def best_config(self):
        """ Get the overall best config, as voted by all benchmark results.
        """
        return self._gemm_config_freq.most_common(1)

    def std(self):
        """ Get the standard deviation as a measure of dispersion of the distribution. We should aim for higher values
        as they indicate there is high variation in the distribution. Thus the evidence of the best config is stronger.
        """
        freqs = self._gemm_config_freq.values()
        if len(freqs) == 0:
            return 0
        mean_freq = sum(freqs) / len(freqs)
        return math.sqrt(sum((freq - mean_freq) ** 2 for freq in freqs) / len(freqs))








GEMM_CONFIG_FACTORY = {
    Strategy.Native: NativeGEMMConfig,
    Strategy.ReshapedOnlyRHS: ReshapedOnlyRHSGEMMConfig,
    Strategy.Reshaped: ReshapedGEMMConfig,
}



EXAMPLE_FILE_2_STRATEGY = {
    "benchmark_cl_gemm_native": Strategy.Native,
    "benchmark_cl_gemm_reshaped_rhs_only": Strategy.ReshapedOnlyRHS,
    "benchmark_cl_gemm_reshaped": Strategy.Reshaped,
}











GEMM_EXAMPLE_ARGS_FACTORY = {
    
    strategy: namedtuple(
        "{}_Gemm_Example_Args".format(strategy_name),
        GEMMParam._fields[:-1] + GEMM_CONFIG_FACTORY[strategy]._fields,
    )
    for strategy_name, strategy in Strategy.__members__.items()
    if strategy_name == strategy.name
}


BENCHMARK_RESULT_JSON_EXTENSION = "gemmtuner_benchmark"






def parse_benchmark_commandline(commandline: str) -> Dict[str, str]:
    """ Parse the benchmark example command-line string into a dictionary of command-line arguments
    """
    
    commandline = commandline.replace(",--type=", " --type=")

    args = commandline.split()
    
    args = args[1:]
    
    args = map(lambda arg: arg.split("="), args)

    def transform(_name):
        "--" if it exists
        _name = _name.lstrip("-")
        return _name

    return {transform(name): val for name, val in args}


def extract_benchmark_results(
    json_results: Dict, measurement_method="avg"
) -> Generator[BenchmarkResult, None, None]:
    """ Parse the benchmark result and extract relevant information, namely:
        GEMM param,
        Strategy,
        GEMM config,
        Measurements
    """
    for json_res in json_results:
        
        
        example_tests = list(json_res["tests"].items())
        assert len(example_tests) == 1
        example_fn, example_test_data = example_tests[0]

        
        example_fn = example_fn.split(os.path.sep)[-1]

        
        strategy = EXAMPLE_FILE_2_STRATEGY[example_fn]

        
        benchmark_args = parse_benchmark_commandline(json_res["CommandLine"])
        Gemm_Example_Args_T = GEMM_EXAMPLE_ARGS_FACTORY[strategy]
        example_args = Gemm_Example_Args_T(
            *(benchmark_args["example_args"].split(",")))
        
        
        gemm_param_fields_len = len(GEMMParam._fields) - 1
        gemm_param = GEMMParam.parse_from_strs(
            *example_args[:gemm_param_fields_len],
            data_type = benchmark_args["type"])
        GEMMConfig = GEMM_CONFIG_FACTORY[strategy]
        gemm_config = GEMMConfig.parse_from_strs(
            *example_args[gemm_param_fields_len:])

        
        measurements = list(example_test_data["measurements"].items())
        
        
        measurement_ms_reshape = 0
        measurement_ms_kernel = 0
        for single_measurement in measurements:
            measurement_instrument, data = single_measurement
            
            measurement_instrument_name = measurement_instrument.split("/")[0]
            assert measurement_instrument_name == "OpenCLTimer"
            
            if measurement_method == "min":
                measurement_val = min(data["raw"])
            elif measurement_method == "avg":
                measurement_val = sum(data["raw"]) / len(data["raw"])
            else:
                raise ValueError(
                    "Invalid measurement method: {}".format(measurement_method)
                )

            measurement_type = measurement_instrument.split("/")[1]
            if "reshape" in measurement_type.split("_"):
                measurement_ms_reshape = measurement_val
            else:
                measurement_ms_kernel = measurement_val

        measurement = Measurement(
            measurement_ms_reshape, measurement_ms_kernel)

        yield BenchmarkResult(gemm_param, strategy, gemm_config, measurement)


def parse_json(dir_name):
    """ Glob all benchmark result json files and parse them into json objects (dicts).
    """
    for res_fn in Path(dir_name).rglob("*.{}".format(BENCHMARK_RESULT_JSON_EXTENSION)):
        with open(res_fn) as res_fp:
            yield json.load(res_fp)


def check_out_path(out_path):
    if os.path.exists(out_path):
        overwrite = (
            input(
                "Output JSON {} already exists. Overwrite? [Y/N]: ".format(
                    out_path)
            ).lower()
            == "y"
        )
        if not overwrite:
            logging.info("Skipping {}".format(out_path))
            return False
    logging.info("Saving JSON file to {}".format(out_path))
    return True


def dump_json(out_path, dict):
    with open(out_path, "w") as f:
        json.dump(dict, f)
    logging.info("Saved")







def main(args):
    logging.info(
        "Searching best gemm configurations from {}".format(
            args.benchmark_results_dir)
    )

    benchmark_results = extract_benchmark_results(
        parse_json(args.benchmark_results_dir)
    )

    
    benchmark_result_recorder = GEMMBenchmarkResultRecorder(tol=args.tolerance)
    for benchmark_result in benchmark_results:
        benchmark_result_recorder.add(benchmark_result)

    if args.debug:
        recorder_sum_level = GEMMBenchmarkResultRecorder.SummaryLevel.Detailed
    else:
        recorder_sum_level = GEMMBenchmarkResultRecorder.SummaryLevel.Short

    
    logging.info(benchmark_result_recorder.summary(
        sum_level=recorder_sum_level))

    
    all_config_dists = benchmark_result_recorder.get_config_distributions()

    logging.info("=== Result ===")
    for strategy, config_dist in all_config_dists.items():
        logging.info("Strategy: {}".format(strategy.name))
        logging.debug("GEMM Config, Votes")
        for config, freq in config_dist.frequency():
            logging.debug("{}, {}".format(config, freq))
        logging.info(
            "Best GEMM Config: {} with std: {}".format(
                config_dist.best_config(), config_dist.std()
            )
        )

    
    if args.output_dir is not None:
        benchmark_result_recorder.save_to_jsons(
            args.output_dir, only_best_config=(not args.debug)
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CL GEMM Tuner")
    parser.add_argument(
        "-b",
        "--benchmark_results",
        dest="benchmark_results_dir",
        metavar="PATH",
        action="store",
        type=str,
        help="Path to benchmark result directory, where benchmark result json files have a file \
                                extension of '{}'".format(
            BENCHMARK_RESULT_JSON_EXTENSION
        ),
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        dest="output_dir",
        metavar="PATH",
        action="store",
        type=str,
        help="Path to directory that holds output JSON files. One for strategy selection and one per strategy for GEMM config selection",
    )
    parser.add_argument(
        "-t",
        "--tolerance",
        action="store",
        type=float,
        default=0.01,
        help="For testing if two GEMMConfigs are equivalent in terms of performance. The tolerance is OpenCL timer in\
        milliseconds. Recommended value: <= 0.1 ms",
    )
    parser.add_argument(
        "-D",
        "--debug",
        dest="debug",
        action="store_true",
        help="Enable script debugging output",
    )
    args = parser.parse_args()
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level)
    logging.debug("Arguments: {}".format(args))
    main(args)
