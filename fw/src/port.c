/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * license and copyright intentionally withheld to promote copying into user code.
 */

#include "FreeRTOS.h"
#include "task.h"

BaseType_t xPortStartScheduler(void)
{
	extern void xPortSwitchToTask(void);

	xPortSwitchToTask();
    return pdFAIL;
}

StackType_t *pxPortInitialiseStack(StackType_t *pxTopOfStack, TaskFunction_t pxCode, void *pvParameters)
{
	( void ) pxTopOfStack;
	( void ) pvParameters;
	( void ) * pxCode;

	pxTopOfStack -= 28;

	// ra
	pxTopOfStack[0] = (StackType_t)pxCode;

	for (int i = 1; i < 28; i++) {
		pxTopOfStack[i] = 0;
	}

	return pxTopOfStack;
}
