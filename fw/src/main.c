/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * https://www.FreeRTOS.org
 * https://github.com/FreeRTOS
 *
 */

/*
 * This is a simple main that will start the FreeRTOS-Kernel and run a periodic task
 * that only delays if compiled with the template port, this project will do nothing.
 * For more information on getting started please look here:
 * https://www.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide
 */

/* FreeRTOS includes. */
#include <FreeRTOS.h>
#include <task.h>
#include <queue.h>
#include <timers.h>
#include <semphr.h>

/* Standard includes. */
#include <stdio.h>

#define TIMER_BASE 0x80001000

/*-----------------------------------------------------------*/

static void exampleTask( void * parameters ) __attribute__( ( noreturn ) );

/*-----------------------------------------------------------*/

static void exampleTask( void * parameters )
{
	/* Unused parameters. */
	( void ) parameters;

	printf("Hi from %s\n", __func__);
	for( ; ; )
	{
		printf("Yielding from %s: %li\n", __func__, pdTICKS_TO_MS(xTaskGetTickCount()));
		vTaskDelay(pdMS_TO_TICKS(1000));
	}
	printf("FATAL ERROR\n");
}

static void exampleTask2( void * parameters )
{
	/* Unused parameters. */
	( void ) parameters;

	printf("Hi from %s\n", __func__);
	for( ; ; )
	{
		printf("Yielding from %s: %li\n", __func__, pdTICKS_TO_MS(xTaskGetTickCount()));
		vTaskDelay(pdMS_TO_TICKS(10000));
	}
	printf("FATAL ERROR\n");
}
/*-----------------------------------------------------------*/

int main( void )
{
	static StaticTask_t exampleTaskTCB;
	static StackType_t exampleTaskStack[ configMINIMAL_STACK_SIZE ];
	static StaticTask_t exampleTask2TCB;
	static StackType_t exampleTask2Stack[ configMINIMAL_STACK_SIZE ];

	( void ) printf( "Example FreeRTOS Project\n" );

	( void ) xTaskCreateStatic( &exampleTask,
			"example",
			configMINIMAL_STACK_SIZE,
			NULL,
			configMAX_PRIORITIES - 1U,
			&( exampleTaskStack[ 0 ] ),
			&( exampleTaskTCB ) );
	( void ) xTaskCreateStatic( &exampleTask2,
			"example2",
			configMINIMAL_STACK_SIZE,
			NULL,
			configMAX_PRIORITIES - 1U,
			&( exampleTask2Stack[ 0 ] ),
			&( exampleTask2TCB ) );

	(void)*((volatile uint32_t *)TIMER_BASE);
	/* Start the scheduler. */
	vTaskStartScheduler();

	printf("FATAL ERROR\n");
	for( ; ; )
	{
		/* Should not reach here. */
	}

	return 0;
}
/*-----------------------------------------------------------*/

void vApplicationIdleHook(void)
{
	uint32_t ticks = *((volatile uint32_t *)TIMER_BASE);

	while (ticks > 0) {
		if (xTaskIncrementTick()) {
			portYIELD();
		}

		ticks--;
	}
}

#if ( configCHECK_FOR_STACK_OVERFLOW > 0 )

void vApplicationStackOverflowHook( TaskHandle_t xTask,
		char * pcTaskName )
{
	/* Check pcTaskName for the name of the offending task,
	 * or pxCurrentTCB if pcTaskName has itself been corrupted. */
	( void ) xTask;
	( void ) pcTaskName;
	printf("FATAL ERROR\n");
}

#endif /* #if ( configCHECK_FOR_STACK_OVERFLOW > 0 ) */
/*-----------------------------------------------------------*/
