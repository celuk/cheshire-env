#!/usr/bin/env bash
# Copyright 2022 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

pargs=""
[[ -n "${BOOTMODE}" ]] && pargs+="+BOOTMODE=${BOOTMODE} "
[[ -n "${PRELMODE}" ]] && pargs+="+PRELMODE=${PRELMODE} "
[[ -n "${BINARY}" ]]   && pargs+="+BINARY=${BINARY} "
[[ -n "${IMAGE}" ]]    && pargs+="+IMAGE=${IMAGE} "
[[ -n "${SELCFG}" ]]   && pargs+="+SelectedCfg=${SELCFG} "

if [ -n "${USE_DRAMSYS}" ] && [ "${USE_DRAMSYS}" == 1 ]; then
    DRAMSYS_ROOT="../dramsys"
    DRAMSYS_LIB="${DRAMSYS_ROOT}/build/lib"
    pargs+=" -sv_lib ${DRAMSYS_LIB}/libDRAMSys_Simulator"
    pargs+=" +DRAMSYS_RES=${DRAMSYS_ROOT}/configs"
fi

COLOR_NC='\e[0m'
COLOR_BLUE='\e[0;34m'

printf ${COLOR_BLUE}"xrun -R ${pargs}"${COLOR_NC}"\n"
xrun -R ${pargs} | tee simulate.log
