/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_COMPILER_MLIR_HLO_INCLUDE_MLIR_HLO_DIALECT_MHLO_TRANSFORMS_PASSES_H_
#define TENSORFLOW_COMPILER_MLIR_HLO_INCLUDE_MLIR_HLO_DIALECT_MHLO_TRANSFORMS_PASSES_H_

#include <memory>

#include "llvm/ADT/ArrayRef.h"

namespace mlir {

class FuncOp;
class ModuleOp;
class Operation;
template <typename T>
class OperationPass;
class Pass;
namespace lmhlo {
class FusionOp;
}  // namespace lmhlo

namespace mhlo {

/// Lowers HLO control flow ops to the Standard dialect.
std::unique_ptr<OperationPass<FuncOp>> createLegalizeControlFlowPass();

/// Lowers from HLO dialect to Standard dialect.
std::unique_ptr<OperationPass<FuncOp>> createLegalizeToStdPass();

/// Lowers from the CHLO dialect to the HLO dialect.
std::unique_ptr<OperationPass<FuncOp>> createChloLegalizeToHloPass(
    bool legalize_broadcasts = true, bool expand_compositions = true);

// canonicalize reduction ops to be suitable for codegen.
std::unique_ptr<OperationPass<FuncOp>> createHloCanonicalizeReductionPass();

/// Lowers from HLO dialect to LHLO dialect allocating/deallocating temporary
/// buffers if necessary.
std::unique_ptr<OperationPass<ModuleOp>> createLegalizeToLhloPass();

/// Lowers from HLO dialect to Memref dialect allocating/deallocating temporary
/// buffers if necessary.
std::unique_ptr<OperationPass<FuncOp>> createLegalizeToMemrefPass();

// Lowers shape operations from HLO dialect to Standard dialect.
std::unique_ptr<OperationPass<FuncOp>>
createLegalizeHloShapeOpsToStandardPass();

// Lowers from HLO dialect to Linalg dialect.
std::unique_ptr<OperationPass<FuncOp>> createLegalizeHloToLinalgPass();

// Lowers from HLO dialects dim operations.
std::unique_ptr<OperationPass<FuncOp>> createLegalizeShapeComputationsPass();

// Sinks constants implicitly captured in control flow regions. This is
// necessary to export to XLA.
std::unique_ptr<OperationPass<FuncOp>> createSinkConstantsToControlFlowPass();

// fuse mhlo ops to kLoop/kInput fusion patterns
std::unique_ptr<OperationPass<FuncOp>> createMhloFusionPass();

/// Lowers trigonometric operations from the standard dialect to approximations
/// that do not use intrinsics.
std::unique_ptr<OperationPass<FuncOp>>
createLegalizeTrigonometricToApproximationPass();

// Move dynamic broadcasts up over element-wise operations and broadcast the
// operands rather than the result. This will eventually allow for larger
// fusions.
std::unique_ptr<OperationPass<FuncOp>> createBroadcastPropagationPass();

// Prepare moving dynamic broadcasts up over element-wise operations and
// broadcast the operands rather than the result. This will eventually allow for
// larger fusions.
std::unique_ptr<OperationPass<FuncOp>> createMergeAssumingOpsPass();

// Group reduction and parallel dimensions of reduction operations and realize
// them through equivalent 1D or 2D reductions.
std::unique_ptr<OperationPass<FuncOp>> createGroupReductionDimensionsPass(
    bool prefer_columns_reductions = true);

/// Rank specialization passes:
///   - Find compatible operations and group them together in one rank
///     specialization cluster.
///   - Lower rank specialization clusters to SCF and ranked operations.
std::unique_ptr<OperationPass<FuncOp>> createRankSpecializationClusterPass();
std::unique_ptr<OperationPass<FuncOp>> createRankSpecializationToSCFPass(
    int64_t max_target_rank = 5);

std::unique_ptr<OperationPass<FuncOp>> createOptimizeMhloPass();
std::unique_ptr<OperationPass<FuncOp>> createLowerComplexPass();
std::unique_ptr<::mlir::Pass> createLegalizeGeneralDotPass();
std::unique_ptr<OperationPass<FuncOp>> createLegalizeEinsumToDotGeneralPass();
std::unique_ptr<OperationPass<FuncOp>>
createLegalizeGatherToTorchIndexSelectPass();
std::unique_ptr<OperationPass<FuncOp>> createFlattenTuplePass();

// Creates a pass for expanding mhlo.tuple ops.
std::unique_ptr<OperationPass<ModuleOp>> CreateExpandHloTuplesPass(
    const std::string& entry_function_name = "main");

}  // namespace mhlo
}  // namespace mlir

#endif  // TENSORFLOW_COMPILER_MLIR_HLO_INCLUDE_MLIR_HLO_DIALECT_MHLO_TRANSFORMS_PASSES_H_
